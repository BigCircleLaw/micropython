#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"
#include "py/mphal.h"

#include "wb-lib/public.h"
#include "wb-lib/syspublic.h"
#include "wb-lib/led.h"


mp_obj_t led_control_red(mp_obj_t self_in) { 	

    led_set_color(RGB_R);
	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(led_control_red_obj, led_control_red);

mp_obj_t led_control_green(mp_obj_t self_in) { 	

    led_set_color(RGB_G);
	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(led_control_green_obj, led_control_green);

mp_obj_t led_control_blue(mp_obj_t self_in) { 	

    led_set_color(RGB_B);
	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(led_control_blue_obj, led_control_blue);

mp_obj_t led_control_light_blue(mp_obj_t self_in) { 	

    led_set_color(RGB_LB);
	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(led_control_light_blue_obj, led_control_light_blue);

mp_obj_t led_control_yellow(mp_obj_t self_in) { 	

    led_set_color(RGB_Y);
	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(led_control_yellow_obj, led_control_yellow);

mp_obj_t led_control_purple(mp_obj_t self_in) { 	

    led_set_color(RGB_P);
	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(led_control_purple_obj, led_control_purple);

mp_obj_t led_control_white(mp_obj_t self_in) { 	

    led_set_color(RGB_W);
	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(led_control_white_obj, led_control_white);

mp_obj_t led_control_off(mp_obj_t self_in) { 	

    led_set_color(RGB_OFF);
	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(led_control_off_obj, led_control_off);

//定义type的locals_dict_type
STATIC const mp_rom_map_elem_t led_control_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR_red), MP_ROM_PTR(&led_control_red_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_green), MP_ROM_PTR(&led_control_green_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_blue), MP_ROM_PTR(&led_control_blue_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_light_blue), MP_ROM_PTR(&led_control_light_blue_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_yellow), MP_ROM_PTR(&led_control_yellow_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_purple), MP_ROM_PTR(&led_control_purple_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_white), MP_ROM_PTR(&led_control_white_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_off), MP_ROM_PTR(&led_control_off_obj)},
};
//这个定义字典的宏定义
STATIC MP_DEFINE_CONST_DICT(led_control_locals_dict, led_control_locals_dict_table);

// const mp_obj_type_t wonderbits_led_control_type;
// STATIC mp_obj_t wonderbits_led_control_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args)
// {
//     mp_arg_check_num(n_args, n_kw, 1, 1, false);   //检查参数个数
//     led_control_content_t *self=m_new_obj(led_control_content_t);       //创建对象，分配空间
//     self->base.type=&wonderbits_led_control_type;           //定义对象的类型
//     return MP_OBJ_FROM_PTR(self);                 //返回对象的指针
// }

//定义一个mp_obj_type_t 类型的结构体。注意这里和定义module使用的类型是不一样的
const mp_obj_type_t wonderbits_led_control_type = {
    .base={ &mp_type_type }, 
    .name = MP_QSTR__led,           //type 类的name属性是放在这里定义的，而不是放在DICT中
    .locals_dict = (mp_obj_dict_t*)&led_control_locals_dict,   //注册math_locals_dict
};
const led_control_content_t mp_const_led_control_obj = {{&wonderbits_led_control_type}, RGB_OFF};
