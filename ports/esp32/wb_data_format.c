#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"
#include "py/mphal.h"

#include "wb-lib/sender.h"
#include "wb-lib/public.h"

typedef struct _data_format_content_t
{
    mp_obj_base_t base;   //定义的对象结构体要包含该成员
    const char * receive_data;
    size_t receive_len;
    
    const unsigned char * send_data;
    size_t send_len;

}data_format_content_t;

//定义DataFormat.get_receive_list函数
mp_obj_t data_format_get_receive_list(mp_obj_t self_in, mp_obj_t data ) { 	
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    data_format_content_t *self=MP_OBJ_TO_PTR(self_in);

    self->receive_data = mp_obj_str_get_data(data, &(self->receive_len));
    

	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(data_format_get_receive_list_obj, data_format_get_receive_list);

//定义DataFormat.get_send_list函数
mp_obj_t data_format_get_send_list(mp_obj_t self_in, mp_obj_t data ) { 	
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    data_format_content_t *self=MP_OBJ_TO_PTR(self_in);
    
    // mp_obj_t *path_items;
    // size_t len;
    // mp_obj_list_get(data, &len, &path_items);
    self->send_data = (const unsigned char *)mp_obj_str_get_data(data, &(self->send_len));

	return mp_const_none;  //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(data_format_get_send_list_obj, data_format_get_send_list);

//定义type的locals_dict_type
STATIC const mp_rom_map_elem_t data_format_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_receive_list), MP_ROM_PTR(&data_format_get_receive_list_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_send_list), MP_ROM_PTR(&data_format_get_send_list_obj)},
    
};
//这个定义字典的宏定义
STATIC MP_DEFINE_CONST_DICT(data_format_locals_dict, data_format_locals_dict_table);

const mp_obj_type_t wonderbits_data_format_type;
STATIC mp_obj_t wonderbits_data_format_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args)
{
    mp_arg_check_num(n_args, n_kw, 1, 1, false);   //检查参数个数
    data_format_content_t *self=m_new_obj(data_format_content_t);       //创建对象，分配空间
    self->base.type=&wonderbits_data_format_type;           //定义对象的类型
    return MP_OBJ_FROM_PTR(self);                 //返回对象的指针
}

//定义一个mp_obj_type_t 类型的结构体。注意这里和定义module使用的类型是不一样的
const mp_obj_type_t wonderbits_data_format_type = {
    .base={ &mp_type_type }, 
    .name = MP_QSTR__DataFormat,           //type 类的name属性是放在这里定义的，而不是放在DICT中
    .make_new = wonderbits_data_format_make_new,
    .locals_dict = (mp_obj_dict_t*)&data_format_locals_dict,   //注册math_locals_dict
};
