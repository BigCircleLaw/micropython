#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"

#include "wb-lib/syspublic.h"
#include "wb-lib/uart.h"

STATIC mp_obj_t modtest_uart_init()
{
    printf("This is wb uart init.\n");
    wb_uart_init();
    printf("Finish.\n");
    return mp_const_none;//不需要返回数据就返回它
}

//每一个我们和python接口的函数都需要使用这个宏定义
STATIC const MP_DEFINE_CONST_FUN_OBJ_0(wb_uart_init_obj,modtest_uart_init);

STATIC mp_obj_t wb_send_a_data(mp_obj_t data)
{
    int c = mp_obj_get_int(data);
    printf("This function have one parameters: 0x%02X\n", c);  //请注意这里从参数中提取整数使用的方法
    UART1_SendByte(c);
    return mp_const_none;  //同样没有返回值
}

//这里使用的宏定义和面的名称不一样，OBJ_1区别
STATIC const MP_DEFINE_CONST_FUN_OBJ_1(wb_send_a_data_obj,wb_send_a_data);

extern const mp_obj_type_t wonderbits_module_obj_type;
extern const mp_obj_type_t wonderbits_data_format_type;
extern const frame_hub_content_t mp_const_frame_hub_obj;
extern const led_control_content_t mp_const_led_control_obj;

//定义的modtest全局字典，之后我们添加type和function就要添加在这里
STATIC const mp_rom_map_elem_t wonderbits_globals_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_wonderbits)},   //这个对应python层面的__name__ 属性
    {MP_OBJ_NEW_QSTR(MP_QSTR_ModuleObj), MP_ROM_PTR(&wonderbits_module_obj_type)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR__DataFormat), MP_ROM_PTR(&wonderbits_data_format_type)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR_hub), MP_ROM_PTR(&mp_const_frame_hub_obj)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR_led), MP_ROM_PTR(&mp_const_led_control_obj)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR_uart_init), MP_ROM_PTR(&wb_uart_init_obj)}, 
    {MP_OBJ_NEW_QSTR(MP_QSTR_send_a_data), MP_ROM_PTR(&wb_send_a_data_obj)}, 
};

//这个可以认为是把modtest_globals_table注册到 mp_module_modtest.globals里面去
STATIC MP_DEFINE_CONST_DICT(mp_module_wonderbits_globals, wonderbits_globals_table);   

//这个是定义一个module类型
const mp_obj_module_t mp_module_wonderbits = {
    .base = {&mp_type_module},    
    .globals = (mp_obj_dict_t *)&mp_module_wonderbits_globals,
};
