#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "py/objarray.h"

#include "wb-lib/sender.h"
#include "wb-lib/public.h"
#include "wb-lib/tool.h"

static bool wb_add_data(unsigned char val_type, unsigned char *buf, mp_obj_t data, unsigned char *num);

typedef struct _data_format_content_t
{
    mp_obj_base_t base; //定义的对象结构体要包含该成员
    const char *receive_data;
    size_t receive_len;

    const unsigned char *send_data;
    size_t send_len;

    unsigned char buffer[MSG_MAX_LENGTH_ALL];
    char buffer_translate[10];
    unsigned char len_translate;
} data_format_content_t;

//定义DataFormat.get_receive_list函数
mp_obj_t data_format_get_receive_list(mp_obj_t self_in, mp_obj_t data)
{
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    data_format_content_t *self = MP_OBJ_TO_PTR(self_in);

    self->receive_data = mp_obj_str_get_data(data, &(self->receive_len));

    return mp_const_none; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(data_format_get_receive_list_obj, data_format_get_receive_list);

//定义DataFormat.get_send_list函数
mp_obj_t data_format_get_send_list(mp_obj_t self_in, mp_obj_t data)
{
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    data_format_content_t *self = MP_OBJ_TO_PTR(self_in);

    mp_obj_t *list_items;
    size_t len;
    mp_obj_list_get(data, &len, &list_items);
    unsigned char count = 0;
    if (self->len_translate != len)
    {
        printf("Format error!");
        return mp_const_none;
    }
    // self->send_data = (const unsigned char *)mp_obj_str_get_data(data, &(self->send_len));
    for (unsigned char i = 0; i < len; i++)
    {
        if (wb_add_data(self->buffer_translate[i], self->buffer, list_items[i], &count))
        {
            printf("Format error! index : %d", i);
        }
    }
    mp_obj_array_t *result = MP_OBJ_TO_PTR(mp_obj_new_memoryview('B',
                                                                 count,
                                                                 self->buffer));

    return MP_OBJ_FROM_PTR(result); //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(data_format_get_send_list_obj, data_format_get_send_list);

//定义type的locals_dict_type
STATIC const mp_rom_map_elem_t data_format_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_data_list), MP_ROM_PTR(&data_format_get_receive_list_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_get_list), MP_ROM_PTR(&data_format_get_send_list_obj)},

};
//这个定义字典的宏定义
STATIC MP_DEFINE_CONST_DICT(data_format_locals_dict, data_format_locals_dict_table);

const mp_obj_type_t wonderbits_data_format_type;
STATIC mp_obj_t wonderbits_data_format_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args)
{
    mp_arg_check_num(n_args, n_kw, 1, 1, false);                    //检查参数个数
    data_format_content_t *self = m_new_obj(data_format_content_t); //创建对象，分配空间
    self->base.type = &wonderbits_data_format_type;                 //定义对象的类型

    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[0], &bufinfo, MP_BUFFER_READ);
    self->len_translate = 10 < bufinfo.len ? 10 : bufinfo.len;

    ustrncpy((unsigned char *)self->buffer_translate, (unsigned char *)bufinfo.buf, self->len_translate);

    return MP_OBJ_FROM_PTR(self); //返回对象的指针
}

//定义一个mp_obj_type_t 类型的结构体。注意这里和定义module使用的类型是不一样的
const mp_obj_type_t wonderbits_data_format_type = {
    .base = {&mp_type_type},
    .name = MP_QSTR__DataFormat, //type 类的name属性是放在这里定义的，而不是放在DICT中
    .make_new = wonderbits_data_format_make_new,
    .locals_dict = (mp_obj_dict_t *)&data_format_locals_dict, //注册math_locals_dict
};

static bool wb_add_data(unsigned char val_type, unsigned char *buf, mp_obj_t data, unsigned char *num)
{
    unsigned char count = *num;
    // unsigned char size = 0;
    // unsigned char temp[4] = {0, 0, 0, 0};
    switch (val_type)
    {
    case 'b':
    case 'B':
    {
        buf[count++] = mp_obj_get_int(data);
        *num = count;
        break;
    }
    case 'h':
    case 'H':
    {
        short val = mp_obj_get_int(data);
        ustrncpy((buf + count), (unsigned char *)&val, 2);
        *num = count + 2;
        break;
    }
    case 'i':
    case 'I':
    {
        int val = mp_obj_get_int(data);
        ustrncpy((buf + count), (unsigned char *)&val, 4);
        *num = count + 4;
        break;
    }
    case 'l':
    case 'L':
    {
        long val = mp_obj_get_int(data);
        ustrncpy((buf + count), (unsigned char *)&val, 4);
        *num = count + 4;
        break;
    }
    // case 'q':
    // case 'Q':
    //     break;
    case 'P':
    case 'O':
    case 'S':
    {
        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(data, &bufinfo, MP_BUFFER_READ);
        unsigned char len = bufinfo.len;
        if (20 < len)
        {
            len = 20;
            printf("S length can't exceed 20");
        }
        ustrncpy((buf + count), (unsigned char *)bufinfo.buf, len);
        *num = count + len;
        break;
    }
    case 'f':
    {
        float val;
        if (mp_obj_get_float_maybe(data, &val))
        {
            ustrncpy((buf + count), (unsigned char *)&val, sizeof(float));
            *num = count + sizeof(float);
        }
        else
        {
            return true;
        }

        break;
    }
        // case 'd':
        //     break;
    default:
        return false;
    }

    return false;
}
