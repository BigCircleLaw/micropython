#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"

#include "wb-lib/syspublic.h"
#include "wb-lib/public.h"
#include "wb-lib/uart.h"
#include "wb-lib/module_manager.h"
#include "wb-lib/led.h"

STATIC mp_obj_t wonderbitd_init()
{
    printf("This is wb init.\n");
    wb_uart_init();
    led_init();
    // module_manager_init();
    printf("Finish.\n");
    return mp_const_none;//不需要返回数据就返回它
}

//每一个我们和python接口的函数都需要使用这个宏定义
STATIC const MP_DEFINE_CONST_FUN_OBJ_0(wonderbitd_init_obj,wonderbitd_init);


STATIC mp_obj_t wb_constrain(mp_obj_t amt, mp_obj_t low, mp_obj_t high)
{

    mp_float_t _amt, _low, _high;

    _amt = mp_obj_get_float(amt);
    _low = mp_obj_get_float(low);
    _high = mp_obj_get_float(high);
    
    if(_amt < _low)
        return low;
    else if(_amt > _high)
        return high;
    else
        return amt;
    
    return mp_const_none;  //同样没有返回值
}

STATIC const MP_DEFINE_CONST_FUN_OBJ_3(wb_constrain_obj,wb_constrain);

extern const mp_obj_type_t wonderbits_data_format_type;
extern const led_control_content_t mp_const_led_control_obj;
extern const module_manager_content_t mp_const_module_manager_obj;
extern const frame_hub_content_t mp_const_frame_hub_obj;

//定义的modtest全局字典，之后我们添加type和function就要添加在这里
STATIC const mp_rom_map_elem_t wonderbits_globals_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_wonderbits)},   //这个对应python层面的__name__ 属性
    {MP_OBJ_NEW_QSTR(MP_QSTR__DataFormat), MP_ROM_PTR(&wonderbits_data_format_type)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR_module_manager), MP_ROM_PTR(&mp_const_module_manager_obj)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR_hub), MP_ROM_PTR(&mp_const_frame_hub_obj)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR_led), MP_ROM_PTR(&mp_const_led_control_obj)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR_init), MP_ROM_PTR(&wonderbitd_init_obj)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR_constrain), MP_ROM_PTR(&wb_constrain_obj)}, 

    
    {MP_OBJ_NEW_QSTR(MP_QSTR__Addr_Master), MP_ROM_INT(Addr_Master)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR__Addr_Broadcast), MP_ROM_INT(Addr_Broadcast)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR__Addr_Error), MP_ROM_INT(Addr_Error)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR__TYPE_INIT), MP_ROM_INT(TYPE_INIT)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR__TYPE_RESPONSE), MP_ROM_INT(TYPE_RESPONSE)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR__TYPE_REQUEST), MP_ROM_INT(TYPE_REQUEST)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR__TYPE_REPORT), MP_ROM_INT(TYPE_REPORT)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR__TYPE_INSERT), MP_ROM_INT(TYPE_INSERT)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR__CMD_LED), MP_ROM_INT(CMD_LED)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR__CMD_GET_VERSION), MP_ROM_INT(CMD_GET_VERSION)}, 
};

//这个可以认为是把modtest_globals_table注册到 mp_module_modtest.globals里面去
STATIC MP_DEFINE_CONST_DICT(mp_module_wonderbits_globals, wonderbits_globals_table);   

//这个是定义一个module类型
const mp_obj_module_t mp_module_wonderbits = {
    .base = {&mp_type_module},    
    .globals = (mp_obj_dict_t *)&mp_module_wonderbits_globals,
};
