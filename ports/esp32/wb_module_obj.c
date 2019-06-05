#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"
#include "py/mphal.h"

#include "wb-lib/sender.h"
#include "wb-lib/public.h"
#include "wb-lib/syspublic.h"


//定义无参数函数
// STATIC mp_obj_t math_nothing()
// {
//     printf("This is a function in class type and no parameter\n");
//     printf("WonderBits\n");
//     return mp_const_none;
// }
// //使用函数参数使用对应宏定义
// STATIC MP_DEFINE_CONST_FUN_OBJ_0(math_nothing_obj,math_nothing);

// //定义ceshi_set_v函数
// mp_obj_t ceshi_set_v(mp_obj_t self_in,mp_obj_t data) { 	
//     math_obj_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
//     self->value1=mp_obj_get_int(data);               
// 	return mp_const_none;  
// }
// //注意两点，我这里使用的是OBJ_2而不是OBJ_1
// STATIC MP_DEFINE_CONST_FUN_OBJ_2(ceshi_set_v_obj, ceshi_set_v);

// //定义ceshi_set_value函数
// mp_obj_t ceshi_set_value(mp_obj_t self_in,mp_obj_t data) { 	
//     math_obj_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
//     self->value2=mp_obj_get_int(data);               
// 	return mp_const_none;  
// }
// //注意两点，我这里使用的是OBJ_2而不是OBJ_1
// STATIC MP_DEFINE_CONST_FUN_OBJ_2(ceshi_set_value_obj, ceshi_set_value);

//定义ModuleObj._get_data函数
mp_obj_t module_get_data(mp_obj_t self_in) { 	
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    // self->value1=100;                    
    // self->value2=mp_obj_get_int(data);    //从第二个参数里面取出整型数值
	return mp_const_none;  //返回计算的结果
}

STATIC MP_DEFINE_CONST_FUN_OBJ_1(module_get_data_obj, module_get_data);

//定义ModuleObj._do_update_value函数
mp_obj_t module_do_update_value(mp_obj_t self_in) { 	
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    // self->value1=100;                    
    // self->value2=mp_obj_get_int(data);    //从第二个参数里面取出整型数值
	return mp_const_none;  //返回计算的结果
}

STATIC MP_DEFINE_CONST_FUN_OBJ_1(module_do_update_value_obj, module_do_update_value);

mp_obj_t module_send_without_ack(size_t n_args, const mp_obj_t *args) { 

    module_obj_content_t *self=MP_OBJ_TO_PTR(args[0]);  //从第一个参数里面取出对象的指针
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[2], &bufinfo, MP_BUFFER_READ);
    sendACK(self->des_addr, mp_obj_get_int(args[1]), bufinfo.buf, bufinfo.len);
	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(module_send_without_ack_obj, 3, 3, module_send_without_ack);

mp_obj_t module_send_with_ack(size_t n_args, const mp_obj_t *args) { 	
    
    module_send_without_ack(n_args, args);
    int delay = mp_obj_get_int(args[3]);
    while(delay > 0)
    {
        mp_hal_delay_ms(10);
        delay -= 10;
    }
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    // self->value1=100;                    
    // self->value2=mp_obj_get_int(data);    //从第二个参数里面取出整型数值
	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(module_send_with_ack_obj, 4, 4, module_send_with_ack);

//定义ModuleObj._do_update_value函数
mp_obj_t module_set_onboard_rgb(mp_obj_t self_in, mp_obj_t rgb ) { 	
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);

    unsigned char data = mp_obj_get_int(rgb);
    
    sendACK(self->des_addr, CMD_LED, &data, 1);
	return mp_const_none;  //返回计算的结果
}

STATIC MP_DEFINE_CONST_FUN_OBJ_2(module_set_onboard_rgb_obj, module_set_onboard_rgb);

//定义ModuleObj._do_update_value函数
mp_obj_t module_get_firmware_version(size_t n_args, const mp_obj_t *args) { 	
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    module_obj_content_t *self=MP_OBJ_TO_PTR(args[0]);

    unsigned char data = 0;
    if (n_args > 1)
        data = mp_obj_get_int(args[1]);
    sendACK(self->des_addr, CMD_GET_VERSION, &data, 1);

    int delay = 500;
    while(delay > 0)
    {
        mp_hal_delay_ms(10);
        delay -= 10;
    }

	return mp_const_none;  //返回计算的结果
}

STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(module_get_firmware_version_obj, 1, 2, module_get_firmware_version);

//定义type的locals_dict_type
STATIC const mp_rom_map_elem_t module_obj_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR__get_data), MP_ROM_PTR(&module_get_data_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR__do_update_value), MP_ROM_PTR(&module_do_update_value_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_send_without_ack), MP_ROM_PTR(&module_send_without_ack_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_send_with_ack), MP_ROM_PTR(&module_send_with_ack_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_set_onboard_rgb), MP_ROM_PTR(&module_set_onboard_rgb_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_firmware_version), MP_ROM_PTR(&module_get_firmware_version_obj)},
};
//这个定义字典的宏定义
STATIC MP_DEFINE_CONST_DICT(module_obj_locals_dict, module_obj_locals_dict_table);

const mp_obj_type_t wonderbits_module_obj_type;
STATIC mp_obj_t wonderbits_module_obj_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args)
{
    mp_arg_check_num(n_args, n_kw, 2, 2, false);   //检查参数个数
    module_obj_content_t *self=m_new_obj(module_obj_content_t);       //创建对象，分配空间
    self->base.type=&wonderbits_module_obj_type;           //定义对象的类型
    self->id = mp_obj_get_int(args[0]);
    return MP_OBJ_FROM_PTR(self);                 //返回对象的指针
}

//定义一个mp_obj_type_t 类型的结构体。注意这里和定义module使用的类型是不一样的
const mp_obj_type_t wonderbits_module_obj_type = {
    .base={ &mp_type_type }, 
    .name = MP_QSTR_ModuleObj,           //type 类的name属性是放在这里定义的，而不是放在DICT中
    .make_new = wonderbits_module_obj_make_new,
    .locals_dict = (mp_obj_dict_t*)&module_obj_locals_dict,   //注册math_locals_dict
};
