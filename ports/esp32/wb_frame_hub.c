#include "stdint.h"
#include "stdio.h"

#include "driver/uart.h"

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

mp_obj_t frame_hub_available(mp_obj_t self_in)
{

    size_t num = hub_available();
    return MP_OBJ_NEW_SMALL_INT(num); //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(frame_hub_available_obj, frame_hub_available);

static unsigned char receiver_data[512];
mp_obj_t frame_hub_handle(mp_obj_t self_in)
{
    #if WONDERBITS_DEBUG
        // printf("frame_hub_handle\n");
    #endif
    size_t num = uart_read_bytes(UART_NUM_2, receiver_data, 512, 0);
    for(size_t i = 0; i < num; i++)
    {
        hub_put(receiver_data[i]);
        #if WONDERBITS_DEBUG
            // printf("0x%02x,", receiver_data[i]);
        #endif
    }

    return MP_OBJ_NEW_SMALL_INT(num); //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(frame_hub_handle_obj, frame_hub_handle);

mp_obj_t frame_hub_set_response(mp_obj_t self_in, mp_obj_t addr, mp_obj_t data)
{

#if WONDERBITS_DEBUG
    printf("frame_hub_get_response\n");
#endif
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(data, &bufinfo, MP_BUFFER_READ);

    response_cache_set(mp_obj_get_int(addr), (unsigned char *)bufinfo.buf);


    return mp_const_none; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_3(frame_hub_set_response_obj, frame_hub_set_response);

mp_obj_t frame_hub_get_response(mp_obj_t self_in, mp_obj_t addr)
{

#if WONDERBITS_DEBUG
    printf("frame_hub_get_response\n");
#endif

    unsigned char *buf = response_cache_get(mp_obj_get_int(addr));
    
    if(NULL == buf)
        return mp_const_none;
    unsigned char len = 4 + buf[3];

    mp_obj_array_t *result = MP_OBJ_TO_PTR(mp_obj_new_memoryview('B',
                                                                 len,
                                                                 buf));

    return MP_OBJ_FROM_PTR(result); //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(frame_hub_get_response_obj, frame_hub_get_response);

//定义type的locals_dict_type
STATIC const mp_rom_map_elem_t frame_hub_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_msg), MP_ROM_PTR(&frame_hub_get_msg_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_available), MP_ROM_PTR(&frame_hub_available_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_handle), MP_ROM_PTR(&frame_hub_handle_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_set_response), MP_ROM_PTR(&frame_hub_set_response_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_response), MP_ROM_PTR(&frame_hub_get_response_obj)},
};
//这个定义字典的宏定义
STATIC MP_DEFINE_CONST_DICT(frame_hub_locals_dict, frame_hub_locals_dict_table);


//定义一个mp_obj_type_t 类型的结构体。注意这里和定义module使用的类型是不一样的
const mp_obj_type_t wonderbits_frame_hub_type = {
    .base = {&mp_type_type},
    .name = MP_QSTR__FrameHub, //type 类的name属性是放在这里定义的，而不是放在DICT中
    .locals_dict = (mp_obj_dict_t *)&frame_hub_locals_dict, //注册math_locals_dict
};
const frame_hub_content_t mp_const_frame_hub_obj = {{&wonderbits_frame_hub_type}};
