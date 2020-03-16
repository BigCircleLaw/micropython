/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2018 Zhang Kaihua(apple_eat@126.com)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#include "driver/mcpwm.h"
#include "driver/gpio.h"
#include "esp_err.h"

#include "py/nlr.h"
#include "py/runtime.h"
#include "py/objstr.h"
#include "modmachine.h"
#include "mphalport.h"
#include "modmusic.h"

#define MCPWM_UNIT_MUSIC      MCPWM_UNIT_1
#define MCPWM_TIMER_MUSIC     MCPWM_TIMER_0
#define MCPWM_PWM_MUSIC       MCPWM0A

#define music_set_frequecty(freq)   mcpwm_set_frequency(MCPWM_UNIT_1, MCPWM_TIMER_0, (freq))
#define music_set_duty(duty)        mcpwm_set_duty(MCPWM_UNIT_1, MCPWM_TIMER_0, MCPWM_OPR_A, (duty))
#define music_acquire_pin(pin)      mcpwm_gpio_init(MCPWM_UNIT_1, MCPWM0A, (pin))
#define music_free_pin(pin)         gpio_reset_pin(pin)

inline void music_init_contorl(void) {
    mcpwm_config_t pwm_config;
    pwm_config.frequency = 500;    //frequency = 50Hz, i.e. for every servo motor time period should be 20ms
    pwm_config.cmpr_a = 0;    //duty cycle of PWMxA = 0
    pwm_config.cmpr_b = 0;    //duty cycle of PWMxb = 0
    pwm_config.counter_mode = MCPWM_UP_COUNTER;
    pwm_config.duty_mode = MCPWM_DUTY_MODE_0;
    mcpwm_init(MCPWM_UNIT_MUSIC, MCPWM_TIMER_MUSIC, &pwm_config);    //Configure PWM0A & PWM0B with above settings
}

#define DEFAULT_BPM      120
#define DEFAULT_TICKS    4 // i.e. 4 ticks per beat
#define DEFAULT_OCTAVE   4 // C4 is middle C
#define DEFAULT_DURATION 4 // Crotchet
#define ARTICULATION_MS  10 // articulation between notes in milliseconds

typedef struct _music_data_t {
    uint16_t bpm;
    uint16_t ticks;

    // store these to simplify the writing process
    uint8_t last_octave;
    uint8_t last_duration;

    // Asynchronous parts.
    volatile uint8_t async_state;
    bool async_loop;
    uint32_t async_wait_ticks;
    uint16_t async_notes_len;
    uint16_t async_notes_index;
    int  async_pin;		
    mp_obj_t async_note;
} music_data_t;

enum {
    ASYNC_MUSIC_STATE_IDLE,
    ASYNC_MUSIC_STATE_NEXT_NOTE,
    ASYNC_MUSIC_STATE_ARTICULATE,
};

#define music_data MP_STATE_PORT(music_data)

STATIC uint32_t start_note(const char *note_str, size_t note_len);

extern volatile uint32_t ticker_ticks_ms;

void mpython_music_tick(void) {
    if (music_data == NULL) {
        // music module not yet imported
        return;
    }

    if (music_data->async_state == ASYNC_MUSIC_STATE_IDLE) {
        // nothing to do
        return;
    }

    if (ticker_ticks_ms < music_data->async_wait_ticks) {
        // need to wait for timeout to expire
        return;
    }

    if (music_data->async_state == ASYNC_MUSIC_STATE_ARTICULATE) {
        // turn off output and rest
        // pwm_set_duty_cycle(music_data->async_pin->name, 0);
        music_set_duty(0);
        music_data->async_wait_ticks = ticker_ticks_ms + ARTICULATION_MS;
        music_data->async_state = ASYNC_MUSIC_STATE_NEXT_NOTE;
    } else if (music_data->async_state == ASYNC_MUSIC_STATE_NEXT_NOTE) {
        // play next note
        if (music_data->async_notes_index >= music_data->async_notes_len) {
            if (music_data->async_loop) {
                music_data->async_notes_index = 0;
            } else {
                music_data->async_state = ASYNC_MUSIC_STATE_IDLE;
                music_free_pin(music_data->async_pin);
                music_data->async_pin = -1;
                return;
            }
        }
        mp_obj_t note;
        if (music_data->async_notes_len == 1) {
            note = music_data->async_note;
        } else {
            note = ((mp_obj_t*)music_data->async_note)[music_data->async_notes_index];
        }
        if (note == mp_const_none) {
            // a rest (is this even used anymore?)
            //pwm_set_duty_cycle(music_data->async_pin->name, 0);
            music_set_duty(0);
            music_data->async_wait_ticks = 60000 / music_data->bpm;
            music_data->async_state = ASYNC_MUSIC_STATE_NEXT_NOTE;
        } else {
            // a note
            mp_uint_t note_len;
            const char *note_str = mp_obj_str_get_data(note, &note_len);
            uint32_t delay_on = start_note(note_str, note_len);
            music_data->async_wait_ticks = ticker_ticks_ms + delay_on;
            music_data->async_notes_index += 1;
            music_data->async_state = ASYNC_MUSIC_STATE_ARTICULATE;
        }
    }
}

STATIC void wait_async_music_idle(void) {
    // wait for the async music state to become idle
    while (music_data->async_state != ASYNC_MUSIC_STATE_IDLE) {
        // allow CTRL-C to stop the music
        if (MP_STATE_VM(mp_pending_exception) != MP_OBJ_NULL) {
            music_data->async_state = ASYNC_MUSIC_STATE_IDLE;
            //pwm_set_duty_cycle(music_data->async_pin->name, 0);
            music_set_duty(0);
            break;
        }
    }
}

STATIC uint32_t start_note(const char *note_str, size_t note_len) {
    mcpwm_set_duty(MCPWM_UNIT_MUSIC, MCPWM_TIMER_MUSIC, MCPWM_OPR_A, 50);

    // [NOTE](#|b)(octave)(:length)
    // technically, c4 is middle c, so we'll go with that...
    // if we define A as 0 and G as 7, then we can use the following
    // array of us periods

    // these are the periods of note4 (the octave ascending from middle c) from A->B then C->G
    STATIC uint16_t periods_us[] = {2273, 2025, 3822, 3405, 3034, 2863, 2551};
    // A#, -, C#, D#, -, F#, G#
    STATIC uint16_t periods_sharps_us[] = {2145, 0, 3608, 3214, 0, 2703, 2408};

    // we'll represent the note as an integer (A=0, G=6)
    // TODO: validate the note
    uint8_t note_index = (note_str[0] & 0x1f) - 1;

    // TODO: the duration and bpm should be persistent between notes
    uint32_t ms_per_tick = (60000 / music_data->bpm) / music_data->ticks;

    int8_t octave = 0;
    bool sharp = false;

    size_t current_position = 1;

    // parse sharp or flat
    if (current_position < note_len && (note_str[current_position] == '#' || note_str[current_position] == 'b')) {
        if (note_str[current_position] == 'b') {
            // make sure we handle wrapping round gracefully
            if (note_index == 0) {
                note_index = 6;
            } else {
                note_index--;
            }

            // handle the unusual edge case of Cb
            if (note_index == 1) {
                octave--;
            }
        }

        sharp = true;
        current_position++;
    }

    // parse the octave
    if (current_position < note_len && note_str[current_position] != ':') {
        // currently this will only work with a one digit number
        // use +=, since the sharp/flat code changes octave to compensate.
        music_data->last_octave = (note_str[current_position] & 0xf);
        current_position++;
    }

    octave += music_data->last_octave;

    // parse the duration
    if (current_position < note_len && note_str[current_position] == ':') {
        // I'll make this handle up to two digits for the time being.
        current_position++;

        if (current_position < note_len) {
            music_data->last_duration = note_str[current_position] & 0xf;

            current_position++;
            if (current_position < note_len) {
                music_data->last_duration *= 10;
                music_data->last_duration += note_str[current_position] & 0xf;
            }
        } else {
            // technically, this should be a syntax error, since this means
            // that no duration has been specified. For the time being,
            // we'll let you off :D
        }
    }
    // play the note!

    // make the octave relative to octave 4
    octave -= 4;

    // 18 is 'r' or 'R'
    if (note_index < 10) {
        uint32_t period;
        if (sharp) {
            if (octave >= 0) {
                period = periods_sharps_us[note_index] >> octave;
            }
            else {
                period = periods_sharps_us[note_index] << -octave;
            }
        } else {
            if (octave >= 0) {
                period = periods_us[note_index] >> octave;
            }
            else {
                period = periods_us[note_index] << -octave;
            }
        }
        //pwm_set_period_us(period);
        music_set_frequecty(1000000/period);
    } else {
        //pwm_set_duty_cycle(pin->name, 0);
        music_set_duty(0);
    }

    // Cut off a short time from end of note so we hear articulation.
    mp_int_t gap_ms = (ms_per_tick * music_data->last_duration) - ARTICULATION_MS;
    if (gap_ms < ARTICULATION_MS) {
        gap_ms = ARTICULATION_MS;
    }
    return gap_ms;
}

STATIC mp_obj_t mpython_music_reset(void) {
    music_data->bpm = DEFAULT_BPM;
    music_data->ticks = DEFAULT_TICKS;
    music_data->last_octave = DEFAULT_OCTAVE;
    music_data->last_duration = DEFAULT_DURATION;
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mpython_music_reset_obj, mpython_music_reset);

STATIC mp_obj_t mpython_music_get_tempo(void) {
    mp_obj_t tempo_tuple[2];

    tempo_tuple[0] = mp_obj_new_int(music_data->bpm);
    tempo_tuple[1] = mp_obj_new_int(music_data->ticks);

    return mp_obj_new_tuple(2, tempo_tuple);
}
MP_DEFINE_CONST_FUN_OBJ_0(mpython_music_get_tempo_obj, mpython_music_get_tempo);

STATIC mp_obj_t mpython_music_stop(mp_uint_t n_args, const mp_obj_t *args) {
    int pin;
    if (n_args == 0) {
        pin = 16;
    } else {
        pin = mp_obj_get_int(args[0]);
    }
    // Raise exception if the pin we are trying to stop is not in a compatible mode.
    if(music_data->async_pin == pin) {
        music_free_pin(pin);
        music_data->async_pin = -1;
        music_data->async_state = ASYNC_MUSIC_STATE_IDLE;
    }
    music_set_duty(0);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mpython_music_stop_obj, 0, 1, mpython_music_stop);

STATIC mp_obj_t mpython_music_play(mp_uint_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_music, MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_pin,   MP_ARG_INT, {.u_int = 16} },
        { MP_QSTR_wait,  MP_ARG_BOOL, {.u_bool = true} },
        { MP_QSTR_loop,  MP_ARG_BOOL, {.u_bool = false} },
    };

    // parse args
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // reset octave and duration so tunes always play the same
    music_data->last_octave = DEFAULT_OCTAVE;
    music_data->last_duration = DEFAULT_DURATION;

    // get either a single note or a list of notes
    mp_uint_t len;
    mp_obj_t *items;
    if (MP_OBJ_IS_STR_OR_BYTES(args[0].u_obj)) {
        len = 1;
        items = &args[0].u_obj;
    } else {
        mp_obj_get_array(args[0].u_obj, &len, &items);
    }

    // Release the previous pin
    if(music_data->async_pin != -1) {
        music_free_pin(music_data->async_pin);
        music_data->async_pin = -1;
    }
    
    // get the pin to play on
    int wanted_pin = args[1].u_int;
    if(!GPIO_IS_VALID_OUTPUT_GPIO(wanted_pin)) {
        mp_raise_ValueError("invalid output pin");
    }
    music_acquire_pin(wanted_pin);
    
    // start the tune running in the background
    music_data->async_state = ASYNC_MUSIC_STATE_IDLE;
    music_data->async_wait_ticks = ticker_ticks_ms;
    music_data->async_loop = args[3].u_bool;
    music_data->async_notes_len = len;
    music_data->async_notes_index = 0;
    if (len == 1) {
        // If a string was passed as a single note then we can't store a pointer
        // to args[0].u_obj, so instead store the single string directly (also
        // works if a tuple/list of one element was passed).
        music_data->async_note = items[0];
    } else {
        music_data->async_note = items;
    }
    music_data->async_pin = wanted_pin;
    music_data->async_state = ASYNC_MUSIC_STATE_NEXT_NOTE;

    if (args[2].u_bool) {
        // wait for tune to finish
        wait_async_music_idle();
    }

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_KW(mpython_music_play_obj, 0, mpython_music_play);

STATIC mp_obj_t mpython_music_pitch(mp_uint_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_frequency, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_duration, MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_pin,    MP_ARG_INT, {.u_int = 16} },
        { MP_QSTR_wait,   MP_ARG_BOOL, {.u_bool = true} },
    };

    // parse args
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // get the parameters
    mp_uint_t frequency = args[0].u_int;
    mp_int_t duration = args[1].u_int;
    int pin = args[2].u_int;
    
    // Update pin modes
    if(music_data->async_pin != -1) {
        music_free_pin(music_data->async_pin);
        music_data->async_pin = -1;
    }
    if(!GPIO_IS_VALID_OUTPUT_GPIO(pin)) {
        mp_raise_ValueError("invalid output pin");
    }
    music_acquire_pin(pin);
    
    bool wait = args[3].u_bool;
    music_set_duty(50);
    if (frequency == 0) {
        music_free_pin(pin);
    } else if (music_set_frequecty(frequency)) {
        music_free_pin(pin);
        mp_raise_ValueError("invalid pitch");
    }
    if (duration >= 0) {
        // use async machinery to stop the pitch after the duration
        music_data->async_state = ASYNC_MUSIC_STATE_IDLE;
        music_data->async_wait_ticks = ticker_ticks_ms + duration;
        music_data->async_loop = false;
        music_data->async_notes_len = 0;
        music_data->async_notes_index = 0;
        music_data->async_note = NULL;
        music_data->async_pin = pin;
        music_data->async_state = ASYNC_MUSIC_STATE_ARTICULATE;

        if (wait) {
            // wait for the pitch to finish
            wait_async_music_idle();
        }
    } else {
        // don't block here, since there's no reason to leave a pitch forever in a blocking C function
    }

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_KW(mpython_music_pitch_obj, 0, mpython_music_pitch);

STATIC mp_obj_t mpython_music_set_tempo(mp_uint_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_ticks, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_bpm,   MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0} },
    };

    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (args[0].u_int != 0) {
        // set ticks
        music_data->ticks = args[0].u_int;
    }

    if (args[1].u_int != 0) {
        music_data->bpm = args[1].u_int;
    }

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_KW(mpython_music_set_tempo_obj, 0, mpython_music_set_tempo);


static mp_obj_t music_init(void) {
    music_data = m_new_obj(music_data_t);
    music_data->bpm = DEFAULT_BPM;
    music_data->ticks = DEFAULT_TICKS;
    music_data->last_octave = DEFAULT_OCTAVE;
    music_data->last_duration = DEFAULT_DURATION;
    music_data->async_state = ASYNC_MUSIC_STATE_IDLE;
    music_data->async_pin = -1;
    music_data->async_note = NULL;

    music_init_contorl();

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(music___init___obj, music_init);

STATIC const mp_map_elem_t mpython_music_locals_dict_table[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_music) },
    { MP_OBJ_NEW_QSTR(MP_QSTR___init__), (mp_obj_t)&music___init___obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_TEST), MP_OBJ_NEW_QSTR(MP_QSTR_value_colon_1)},

    { MP_OBJ_NEW_QSTR(MP_QSTR_reset), (mp_obj_t)&mpython_music_reset_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_set_tempo), (mp_obj_t)&mpython_music_set_tempo_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_get_tempo), (mp_obj_t)&mpython_music_get_tempo_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_play), (mp_obj_t)&mpython_music_play_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_pitch), (mp_obj_t)&mpython_music_pitch_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_stop), (mp_obj_t)&mpython_music_stop_obj },
    
    { MP_OBJ_NEW_QSTR(MP_QSTR_DADADADUM), (mp_obj_t)&mpython_music_tune_dadadadum_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ENTERTAINER), (mp_obj_t)&mpython_music_tune_entertainer_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_PRELUDE), (mp_obj_t)&mpython_music_tune_prelude_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ODE), (mp_obj_t)&mpython_music_tune_ode_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_NYAN), (mp_obj_t)&mpython_music_tune_nyan_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_RINGTONE), (mp_obj_t)&mpython_music_tune_ringtone_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_FUNK), (mp_obj_t)&mpython_music_tune_funk_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_BLUES), (mp_obj_t)&mpython_music_tune_blues_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_BIRTHDAY), (mp_obj_t)&mpython_music_tune_birthday_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_WEDDING), (mp_obj_t)&mpython_music_tune_wedding_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_FUNERAL), (mp_obj_t)&mpython_music_tune_funeral_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_PUNCHLINE), (mp_obj_t)&mpython_music_tune_punchline_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_PYTHON), (mp_obj_t)&mpython_music_tune_python_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_BADDY), (mp_obj_t)&mpython_music_tune_baddy_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CHASE), (mp_obj_t)&mpython_music_tune_chase_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_BA_DING), (mp_obj_t)&mpython_music_tune_ba_ding_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_WAWAWAWAA), (mp_obj_t)&mpython_music_tune_wawawawaa_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_JUMP_UP), (mp_obj_t)&mpython_music_tune_jump_up_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_JUMP_DOWN), (mp_obj_t)&mpython_music_tune_jump_down_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_POWER_UP), (mp_obj_t)&mpython_music_tune_power_up_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_POWER_DOWN), (mp_obj_t)&mpython_music_tune_power_down_obj },
    
    { MP_OBJ_NEW_QSTR(MP_QSTR_GE_CHANG_ZU_GUO), (mp_obj_t)&mpython_music_tune_ge_chang_zu_guo_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_DONG_FANG_HONG), (mp_obj_t)&mpython_music_tune_dong_fang_hong_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CAI_YUN_ZHUI_YUE), (mp_obj_t)&mpython_music_tune_cai_yun_zhui_yue_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ZOU_JIN_XIN_SHI_DAI), (mp_obj_t)&mpython_music_tune_zou_jin_xin_shi_dai_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_MO_LI_HUA), (mp_obj_t)&mpython_music_tune_mo_li_hua_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_YI_MENG_SHAN_XIAO_DIAO), (mp_obj_t)&mpython_music_tune_yi_meng_shan_xiao_diao_obj },
};

STATIC MP_DEFINE_CONST_DICT(mpython_music_locals_dict, mpython_music_locals_dict_table);

const mp_obj_module_t mp_music_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mpython_music_locals_dict,
};