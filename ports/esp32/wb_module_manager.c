#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"
#include "py/mphal.h"

#include "wb-lib/sender.h"
#include "wb-lib/public.h"
#include "wb-lib/syspublic.h"
#include "wb-lib/module_manager.h"

#include "wb-lib/uart.h"

//定义ceshi_set_value函数
mp_obj_t module_manager_get_addr(mp_obj_t self_in, mp_obj_t id, mp_obj_t type)
{
    // math_obj_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针

    unsigned char _id = mp_obj_get_int(id);
    unsigned char _type = mp_obj_get_int(type);

    return MP_OBJ_NEW_SMALL_INT(module_manager_getAddr(_id, _type));
}
//注意两点，我这里使用的是OBJ_2而不是OBJ_1
STATIC MP_DEFINE_CONST_FUN_OBJ_3(module_manager_get_addr_obj, module_manager_get_addr);

mp_obj_t module_send_ack(size_t n_args, const mp_obj_t *args)
{

    // module_manager_content_t *self=MP_OBJ_TO_PTR(args[0]);  //从第一个参数里面取出对象的指针
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[3], &bufinfo, MP_BUFFER_READ);
    sendACK(mp_obj_get_int(args[1]), mp_obj_get_int(args[2]), bufinfo.buf, bufinfo.len);
    return mp_const_none; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(module_send_ack_obj, 4, 4, module_send_ack);

mp_obj_t module_manager_start(mp_obj_t self_in)
{
    // module_manager_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    // module_manager_content_t *self=MP_OBJ_TO_PTR(self_in);
    module_manager_init();
    return mp_const_none; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(module_manager_start_obj, module_manager_start);

mp_obj_t wb_module_manager_put(mp_obj_t self_in, mp_obj_t data)
{
    // module_manager_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(data, &bufinfo, MP_BUFFER_READ);
    module_manager_put(((unsigned char *)bufinfo.buf + 4), *((unsigned char *)bufinfo.buf + 3));
    return mp_const_none; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(module_manager_put_obj, wb_module_manager_put);

mp_obj_t wb_module_manager_get_type_num_buf(mp_obj_t self_in)
{
    // module_manager_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    // UART1_SendByte(1);
    unsigned char *data = module_manager_sendTypeAddrtoPC();
    // UART1_SendByte(2);
    if(data == NULL)
    {
        printf("MEN fail!");
        return mp_const_none;
    }
    mp_obj_t ptr = mp_obj_new_bytes((const unsigned char *)data, data[0] * 2 + 1);
    return ptr; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(module_manager_get_type_num_buf_obj, wb_module_manager_get_type_num_buf);

//定义type的locals_dict_type
STATIC const mp_rom_map_elem_t module_manager_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR_send_ack), MP_ROM_PTR(&module_send_ack_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_start), MP_ROM_PTR(&module_manager_start_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_put), MP_ROM_PTR(&module_manager_put_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_addr), MP_ROM_PTR(&module_manager_get_addr_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_type_num_buf), MP_ROM_PTR(&module_manager_get_type_num_buf_obj)},
};
//这个定义字典的宏定义
STATIC MP_DEFINE_CONST_DICT(module_manager_locals_dict, module_manager_locals_dict_table);

const mp_obj_type_t wonderbits_module_manager_type;
STATIC mp_obj_t wonderbits_module_manager_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args)
{
    mp_arg_check_num(n_args, n_kw, 2, 2, false);                          //检查参数个数
    module_manager_content_t *self = m_new_obj(module_manager_content_t); //创建对象，分配空间
    self->base.type = &wonderbits_module_manager_type;                    //定义对象的类型

    return MP_OBJ_FROM_PTR(self); //返回对象的指针
}

//定义一个mp_obj_type_t 类型的结构体。注意这里和定义module使用的类型是不一样的
const mp_obj_type_t wonderbits_module_manager_type = {
    .base = {&mp_type_type},
    .name = MP_QSTR_ModuleManager, //type 类的name属性是放在这里定义的，而不是放在DICT中
    .make_new = wonderbits_module_manager_make_new,
    .locals_dict = (mp_obj_dict_t *)&module_manager_locals_dict, //注册math_locals_dict
};

const module_manager_content_t mp_const_module_manager_obj = {{&wonderbits_module_manager_type}};
