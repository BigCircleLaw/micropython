/*
 * @Author: your name
 * @Date: 2020-03-16 11:19:05
 * @LastEditTime: 2020-04-28 18:14:21
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \wb-micropython\ports\esp32\mod_mpython_sound.c
 */

#include "driver/gpio.h"
#include "driver/adc.h"

#include "py/runtime.h"
#include "py/mphal.h"

const mp_obj_type_t wb_mpython_sound_type;

typedef struct _sound_obj_t
{
    mp_obj_base_t base;
    gpio_num_t gpio_id;
    adc1_channel_t adc1_id;
} sound_obj_t;

typedef struct _madc_obj_t
{
    mp_obj_base_t base;
    gpio_num_t gpio_id;
    adc1_channel_t adc1_id;
} madc_obj_t;

STATIC mp_obj_t sound_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args)
{

    sound_obj_t *self = m_new_obj(sound_obj_t);
    madc_obj_t *o = args[0];
    self->base.type = &wb_mpython_sound_type;
    self->gpio_id = o->gpio_id;
    self->adc1_id = o->adc1_id;

    esp_err_t err = adc1_config_channel_atten(self->adc1_id, ADC_ATTEN_11db);
    if (err == ESP_OK)
    {
        return MP_OBJ_FROM_PTR(self);
    }
    mp_raise_ValueError(MP_ERROR_TEXT("Parameter Error"));
}

int RC_Filter(int curentData, int lastData, float A)
{
    return (int)((1 - A) * curentData + A * lastData);
}

/*希尔排序*/
void shell_sort(int *arr, int bgn, int end)
{
    for (int step = (end - bgn) / 2; step > 0; step /= 2)
    {
        for (int i = bgn; i < bgn + step; ++i)
        {
            /*
    * 以下，insertSort的变异
    */
            for (int j = i + step; j < end; j += step)
            {
                int k = j - step;
                for (; k >= i; k -= step)
                    if (arr[k] <= arr[j])
                        break;
                if (k != j - step)
                {
                    short tmp = arr[j];
                    for (int m = j; m > k + step; m -= step)
                        arr[m] = arr[m - step];
                    arr[k + step] = tmp;
                }
            }
        }
    }
}

STATIC mp_obj_t sound_read(size_t n_args, const mp_obj_t *args)
{
    sound_obj_t *self = args[0];
    int val;
    int record[100];
    int delay = 20;
    record[0] = adc1_get_raw(self->adc1_id);
    if (n_args > 3)
        delay = MP_OBJ_SMALL_INT_VALUE(args[3]);
    for (unsigned char i = 1; i < 100; i++)
    {
        val = adc1_get_raw(self->adc1_id);
        if (val == -1)
        {
            mp_raise_ValueError(MP_ERROR_TEXT("Parameter Error"));
        }
        // printf("%d\n",val);
        record[i] = RC_Filter(val, record[i - 1], 0.4f);
        mp_hal_delay_us(delay);
    }
    // printf("val=%d\n",val);
    shell_sort(record, 0,100);
    if (n_args > 1)
    {
        int min = MP_OBJ_SMALL_INT_VALUE(args[1]);
        int max = MP_OBJ_SMALL_INT_VALUE(args[2]);
        val = record[max] - record[min];
        if(n_args > 4)
            for (unsigned char i = 1; i < 100; i++)
                printf("%d\n",record[i]);
    }
    else
    {
        val = (record[90] - record[10]) / 2;
    }
    
    return MP_OBJ_NEW_SMALL_INT(val);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(sound_read_obj, 1, 5, sound_read);

STATIC const mp_rom_map_elem_t sound_locals_dict_table[] = {

    {MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&sound_read_obj)},
};

STATIC MP_DEFINE_CONST_DICT(sound_locals_dict, sound_locals_dict_table);

const mp_obj_type_t wb_mpython_sound_type = {
    {&mp_type_type},
    .name = MP_QSTR_Sound,
    .make_new = sound_make_new,
    .locals_dict = (mp_obj_t)&sound_locals_dict,
};
