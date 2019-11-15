#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"

#include "wb-lib/syspublic.h"
#include "wb-lib/public.h"
#include "wb-lib/uart.h"
#include "wb-lib/module_manager.h"
#include "wb-lib/led.h"
#include "wb-lib/hub.h"
#include "mpconfigport.h"

#include "freertos/task.h"

STATIC mp_obj_t wonderbitd_init()
{
    printf("This is wb init.\n");
    printf("portTICK_PERIOD_MS's value is %d.\n", portTICK_PERIOD_MS);
    hub_init();
    led_set_color(RGB_OFF);
    // module_manager_init();
    printf("Finish.\n");
    return mp_const_none; //不需要返回数据就返回它
}

//每一个我们和python接口的函数都需要使用这个宏定义
STATIC const MP_DEFINE_CONST_FUN_OBJ_0(wonderbitd_init_obj, wonderbitd_init);

STATIC mp_obj_t wb_constrain(mp_obj_t amt, mp_obj_t low, mp_obj_t high)
{

    mp_float_t _amt, _low, _high;

    _amt = mp_obj_get_float(amt);
    _low = mp_obj_get_float(low);
    _high = mp_obj_get_float(high);

    if (_amt < _low)
        return low;
    else if (_amt > _high)
        return high;
    else
        return amt;

    return mp_const_none; //同样没有返回值
}

STATIC const MP_DEFINE_CONST_FUN_OBJ_3(wb_constrain_obj, wb_constrain);

STATIC mp_obj_t wb_wb_map(size_t n_args, const mp_obj_t *args)
{
    mp_float_t _x, _in_min, _in_max, _out_min, _out_max;
    _x = mp_obj_get_float(args[0]);
    _in_min = mp_obj_get_float(args[1]);
    _in_max = mp_obj_get_float(args[2]);
    _out_min = mp_obj_get_float(args[3]);
    _out_max = mp_obj_get_float(args[4]);
    mp_float_t result = (_x - _in_min) * (_out_max - _out_min) / (_in_max - _in_min) + _out_min;
    return MP_OBJ_FROM_PTR(mp_obj_new_float(result));
}

MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(wb_wb_map_obj, 5, 5, wb_wb_map);

mp_obj_t wb_module_manager_send_a_data(mp_obj_t data)
{
    // module_manager_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    UART1_SendByte(mp_obj_get_int(data));
    return mp_const_none; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(module_manager_send_a_data_obj, wb_module_manager_send_a_data);

mp_obj_t wb__task_switch_then_back(void)
{
    MICROPY_EVENT_POLL_HOOK
    // ulTaskNotifyTake(pdFALSE, 1);
    vTaskDelay(1);
    return mp_const_none; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(task_switch_then_back_obj, wb__task_switch_then_back);

extern const mp_obj_type_t wonderbits_data_format_type;
extern const led_control_content_t mp_const_led_control_obj;
extern const module_manager_content_t mp_const_module_manager_obj;
extern const frame_hub_content_t mp_const_frame_hub_obj;

//定义的modtest全局字典，之后我们添加type和function就要添加在这里
STATIC const mp_rom_map_elem_t wonderbits_globals_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_wb)}, //这个对应python层面的__name__ 属性
    {MP_OBJ_NEW_QSTR(MP_QSTR__DataFormat), MP_ROM_PTR(&wonderbits_data_format_type)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_module_manager), MP_ROM_PTR(&mp_const_module_manager_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_hub), MP_ROM_PTR(&mp_const_frame_hub_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_led), MP_ROM_PTR(&mp_const_led_control_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_init), MP_ROM_PTR(&wonderbitd_init_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_constrain), MP_ROM_PTR(&wb_constrain_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_wb_map), MP_ROM_PTR(&wb_wb_map_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_send_a_data), MP_ROM_PTR(&module_manager_send_a_data_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_task_switch_then_back), MP_ROM_PTR(&task_switch_then_back_obj)},

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
