#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "py/objarray.h"
#include "py/objstr.h"

#include "wb-lib/sender.h"
#include "wb-lib/public.h"
#include "wb-lib/tool.h"

static bool wb_add_data(unsigned char val_type, unsigned char *buf, mp_obj_t data, unsigned char *num);
static mp_obj_t wb_add_list(unsigned char val_type, unsigned char *buf, unsigned char *num, unsigned char len);

STATIC mp_obj_list_t *new_list(size_t n)
{
    mp_obj_list_t *o = m_new_obj(mp_obj_list_t);
    mp_obj_list_init(o, n);
    return o;
}
#define BUFFER_TRANSLATE_MAX 20
typedef struct _data_format_content_t
{
    mp_obj_base_t base; //定义的对象结构体要包含该成员

    unsigned char buffer[MSG_MAX_LENGTH_ALL];
    char buffer_translate[BUFFER_TRANSLATE_MAX];
    unsigned char len_translate;
} data_format_content_t;

//定义DataFormat.get_receive_list函数
mp_obj_t data_format_get_receive_list(mp_obj_t self_in, mp_obj_t data)
{
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    data_format_content_t *self = MP_OBJ_TO_PTR(self_in);

#if WONDERBITS_DEBUG
    printf("receive list\n");
#endif
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(data, &bufinfo, MP_BUFFER_READ);
    unsigned char count = 0;
    mp_obj_list_t *list = new_list(self->len_translate);

#if WONDERBITS_DEBUG
    printf("length : %d\n", self->len_translate);
#endif

    for (unsigned char i = 0; i < self->len_translate; i++)
    {
        list->items[i] = wb_add_list(self->buffer_translate[i], bufinfo.buf, &count, 0);
#if WONDERBITS_DEBUG
        printf("list : %c:%d,", self->buffer_translate[i], ((unsigned char *)bufinfo.buf)[i]);
#endif
    }
#if WONDERBITS_DEBUG
    printf("\n");
#endif

    return MP_OBJ_FROM_PTR(list); //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(data_format_get_receive_list_obj, data_format_get_receive_list);

//定义DataFormat.get_send_list函数
mp_obj_t data_format_get_send_list(mp_obj_t self_in, mp_obj_t data)
{
    // module_obj_content_t *self=MP_OBJ_TO_PTR(self_in);  //从第一个参数里面取出对象的指针
    data_format_content_t *self = MP_OBJ_TO_PTR(self_in);

#if WONDERBITS_DEBUG
    printf("get_send_list\n");
#endif

    mp_obj_t *list_items;
    size_t len;
    mp_obj_list_get(data, &len, &list_items);
    unsigned char count = 0;
    if (self->len_translate != len)
    {
        printf("Format error!\n");
        return mp_const_none;
    }
    for (unsigned char i = 0; i < len; i++)
    {
        if (wb_add_data(self->buffer_translate[i], self->buffer, list_items[i], &count))
        {
            printf("Format error! index : %d\n", i);
        }
    }
#if WONDERBITS_DEBUG
    printf("data : ");
    for (unsigned char i = 0; i < count; i++)
    {
        printf("%d,", self->buffer[i]);
    }
    printf("\n");
#endif
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
    self->len_translate = BUFFER_TRANSLATE_MAX < bufinfo.len ? BUFFER_TRANSLATE_MAX : bufinfo.len;

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

static mp_obj_t wb_add_list(unsigned char val_type, unsigned char *buf, unsigned char *num, unsigned char len)
{
    unsigned char count = *num;
    mp_obj_t data = mp_const_none;
    // unsigned char size = 0;
    // unsigned char temp[4] = {0, 0, 0, 0};
    switch (val_type)
    {
    case 'b':
    case 'B':
    {
        int val = buf[count];
        data = mp_obj_new_int(val);
        *num = count + 1;
        break;
    }
    case 'h':
    case 'H':
    {
        short val = *(short *)(buf + count);
        data = mp_obj_new_int(val);
        *num = count + 2;
        break;
    }
    case 'i':
    case 'I':
    {
        int val = *(int *)(buf + count);
        data = mp_obj_new_int(val);
        *num = count + 4;
        break;
    }
    case 'l':
    case 'L':
    {
        long val = *(long *)(buf + count);
        data = mp_obj_new_int(val);
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
        unsigned char i;
        for(i = 0; buf[count + i] != 0; i++);
        data = mp_obj_new_str_copy(&mp_type_str,&buf[count], i);
        *num = count + i + 1;
        
        break;
    }
    case 'f':
    {
        float val = *(float *)(buf + count);
        data = mp_obj_new_float(val);
        *num = count + 4;
        break;
    }
        // case 'd':
        //     break;
    default:
        return data;
    }

    return data;
}

static bool wb_add_data(unsigned char val_type, unsigned char *buf, mp_obj_t data, unsigned char *num)
{
    unsigned char count = *num;
    // unsigned char size = 0;
    // unsigned char temp[4] = {0, 0, 0, 0};
    float val_float = 0;
    switch (val_type)
    {
    case 'b':
    case 'B':
    case 'h':
    case 'H':
    case 'i':
    case 'I':
    case 'l':
    case 'L':
    case 'f':
        if (!(mp_obj_get_float_maybe(data, &val_float)))
        {
            printf("parameter is not number! ");
            return true;
        }
        break;
    default:;
    }
    switch (val_type)
    {
    case 'b':
    case 'B':
    {
        buf[count++] = (unsigned char)val_float;
        *num = count;
        break;
    }
    case 'h':
    case 'H':
    {
        short val = (short)val_float;
        ustrncpy((buf + count), (unsigned char *)&val, 2);
        *num = count + 2;
        break;
    }
    case 'i':
    case 'I':
    {
        int val = (int)val_float;
        ustrncpy((buf + count), (unsigned char *)&val, 4);
        *num = count + 4;
        break;
    }
    case 'l':
    case 'L':
    {
        long val = (long)val_float;
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
            printf("S length can't exceed 20\n");
        }
        ustrncpy((buf + count), (unsigned char *)bufinfo.buf, len);
        *num = count + len;
        break;
    }
    case 'f':
    {
        float val = val_float;
        ustrncpy((buf + count), (unsigned char *)&val, sizeof(float));
        *num = count + sizeof(float);
        break;
    }
        // case 'd':
        //     break;
    default:
        return false;
    }

    return false;
}
