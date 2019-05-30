#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"

typedef struct _math_obj_t
{
    mp_obj_base_t base;   //定义的对象结构体要包含该成员
    uint16_t value1;      //下面的成员，根据需要自己添加
    uint16_t value2;
    uint16_t _value3;
}math_obj_t;

//定义无参数函数
STATIC mp_obj_t math_nothing()
{
    printf("This is a function in class type and no parameter\n");
    printf("WonderBits\n");
    return mp_const_none;
}
//使用函数参数使用对应宏定义
STATIC MP_DEFINE_CONST_FUN_OBJ_0(math_nothing_obj,math_nothing);

//定义ceshi_set_v函数
mp_obj_t ceshi_set_v(mp_obj_t self_in,mp_obj_t data) { 	
    math_obj_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    self->value1=mp_obj_get_int(data);               
	return mp_const_none;  
}
//注意两点，我这里使用的是OBJ_2而不是OBJ_1
STATIC MP_DEFINE_CONST_FUN_OBJ_2(ceshi_set_v_obj, ceshi_set_v);

//定义ceshi_set_value函数
mp_obj_t ceshi_set_value(mp_obj_t self_in,mp_obj_t data) { 	
    math_obj_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    self->value2=mp_obj_get_int(data);               
	return mp_const_none;  
}
//注意两点，我这里使用的是OBJ_2而不是OBJ_1
STATIC MP_DEFINE_CONST_FUN_OBJ_2(ceshi_set_value_obj, ceshi_set_value);

//定义math_add函数
mp_obj_t math_add(mp_obj_t self_in) { 	
    math_obj_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    // self->value1=100;                    
    // self->value2=mp_obj_get_int(data);    //从第二个参数里面取出整型数值
	printf("%d+%d=", self->value1, self->value2);
	return mp_obj_new_int(self->value1+self->value2);  //返回计算的结果
}

STATIC MP_DEFINE_CONST_FUN_OBJ_1(math_add_obj, math_add);

//定义type的locals_dict_type
STATIC const mp_rom_map_elem_t math_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR_nothing), MP_ROM_PTR(&math_nothing_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_set_value1), MP_ROM_PTR(&ceshi_set_v_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_set_value2), MP_ROM_PTR(&ceshi_set_value_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_add), MP_ROM_PTR(&math_add_obj)},
};
//这个定义字典的宏定义
STATIC MP_DEFINE_CONST_DICT(math_locals_dict, math_locals_dict_table);

const mp_obj_type_t modtest_math_type;
STATIC mp_obj_t modtest_math_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args)
{
    mp_arg_check_num(n_args, n_kw, 0, 0, true);   //检查参数个数
    math_obj_t *self=m_new_obj(math_obj_t);       //创建对象，分配空间
    self->base.type=&modtest_math_type;           //定义对象的类型
    return MP_OBJ_FROM_PTR(self);                 //返回对象的指针
}

//定义一个mp_obj_type_t 类型的结构体。注意这里和定义module使用的类型是不一样的
const mp_obj_type_t modtest_math_type = {
    .base={ &mp_type_type }, 
    .name = MP_QSTR_ceshi,           //type 类的name属性是放在这里定义的，而不是放在DICT中
    .make_new = modtest_math_make_new,
    .locals_dict = (mp_obj_dict_t*)&math_locals_dict,   //注册math_locals_dict
};
