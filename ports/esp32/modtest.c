#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"

STATIC mp_obj_t modtest_test0()
{
    printf("This is wbtest function :test0\n");
    return mp_const_none;//不需要返回数据就返回它
}

//每一个我们和python接口的函数都需要使用这个宏定义
STATIC const MP_DEFINE_CONST_FUN_OBJ_0(modtest_obj_test0,modtest_test0);

STATIC mp_obj_t modtest_test1(mp_obj_t data)
{
    printf("This function have one parameters: %d\n",mp_obj_get_int(data));  //请注意这里从参数中提取整数使用的方法
    return mp_const_none;  //同样没有返回值
}

//这里使用的宏定义和面的名称不一样，OBJ_1区别
STATIC const MP_DEFINE_CONST_FUN_OBJ_1(modtest_obj_test1,modtest_test1);

//定义的modtest全局字典，之后我们添加type和function就要添加在这里
STATIC const mp_rom_map_elem_t modtest_globals_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_wbtest)},   //这个对应python层面的__name__ 属性
    {MP_OBJ_NEW_QSTR(MP_QSTR_test0), MP_ROM_PTR(&modtest_obj_test0)},   //这条是我们添加的，把新建的函数注册进modtest里面去
    {MP_OBJ_NEW_QSTR(MP_QSTR_wb_test1), MP_ROM_PTR(&modtest_obj_test1)},    //把新定义的函数注册进modtest_globals_table
};

//这个可以认为是把modtest_globals_table注册到 mp_module_modtest.globals里面去
STATIC MP_DEFINE_CONST_DICT(mp_module_modtest_globals, modtest_globals_table);   

//这个是定义一个module类型
const mp_obj_module_t mp_module_wbtest = {
    .base = {&mp_type_module},    
    .globals = (mp_obj_dict_t *)&mp_module_modtest_globals,
};
