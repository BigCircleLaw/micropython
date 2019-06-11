#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "py/objarray.h"

#include "wb-lib/public.h"
#include "wb-lib/syspublic.h"
#include "wb-lib/hub.h"

mp_obj_t frame_hub_get_msg(mp_obj_t self_in)
{

    // frame_hub_content_t *self=MP_OBJ_TO_PTR(self_in);    //从第一个参数里面取出对象的指针
    unsigned char *buf = hub_distribute();
    if (buf != NULL)
    {
        mp_obj_array_t *self = MP_OBJ_TO_PTR(mp_obj_new_memoryview('B',
                                                                   MSG_MAX_LENGTH_ALL,
                                                                   buf));
        return MP_OBJ_FROM_PTR(self); //返回计算的结果
    }
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(frame_hub_get_msg_obj, frame_hub_get_msg);

//定义DataFormat.get_send_list函数
mp_obj_t frame_hub_available(mp_obj_t self_in)
{

    // frame_hub_content_t *self=MP_OBJ_TO_PTR(self_in);    //从第一个参数里面取出对象的指针
    size_t num = hub_available();
    return MP_OBJ_NEW_SMALL_INT(num); //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(frame_hub_available_obj, frame_hub_available);

//定义type的locals_dict_type
STATIC const mp_rom_map_elem_t frame_hub_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_msg), MP_ROM_PTR(&frame_hub_get_msg_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_available), MP_ROM_PTR(&frame_hub_available_obj)},
};
//这个定义字典的宏定义
STATIC MP_DEFINE_CONST_DICT(frame_hub_locals_dict, frame_hub_locals_dict_table);

// const mp_obj_type_t wonderbits_frame_hub_type;
// STATIC mp_obj_t wonderbits_frame_hub_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args)
// {
//     mp_arg_check_num(n_args, n_kw, 1, 1, false);   //检查参数个数
//     frame_hub_content_t *self=m_new_obj(frame_hub_content_t);       //创建对象，分配空间
//     self->base.type=&wonderbits_frame_hub_type;           //定义对象的类型
//     return MP_OBJ_FROM_PTR(self);                 //返回对象的指针
// }

//定义一个mp_obj_type_t 类型的结构体。注意这里和定义module使用的类型是不一样的
const mp_obj_type_t wonderbits_frame_hub_type = {
    .base = {&mp_type_type},
    .name = MP_QSTR__FrameHub, //type 类的name属性是放在这里定义的，而不是放在DICT中
    // .make_new = wonderbits_frame_hub_make_new,
    .locals_dict = (mp_obj_dict_t *)&frame_hub_locals_dict, //注册math_locals_dict
};
const frame_hub_content_t mp_const_frame_hub_obj = {{&wonderbits_frame_hub_type}};
