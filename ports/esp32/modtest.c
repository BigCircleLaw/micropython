#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"
//定义的modtest全局字典，之后我们添加type和function就要添加在这里
STATIC const mp_rom_map_elem_t modtest_globals_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_wbtest)},   //这个对应python层面的__name__ 属性
};
//这个可以认为是把modtest_globals_table注册到 mp_module_modtest.globals里面去
STATIC MP_DEFINE_CONST_DICT(mp_module_modtest_globals, modtest_globals_table);   

//这个是定义一个module类型
const mp_obj_module_t mp_module_wbtest = {
    .base = {&mp_type_module},    
    .globals = (mp_obj_dict_t *)&mp_module_modtest_globals,
};
