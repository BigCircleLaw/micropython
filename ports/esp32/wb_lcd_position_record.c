/*
 * @Author: BigCircle
 * @Date: 2020-02-24 17:53:05
 * @LastEditTime: 2020-02-25 15:23:52
 * @LastEditors: Please set LastEditors
 * @Description: 用于做
 * @FilePath: \wb-micropython\ports\esp32\wb_lcd_position_record.c
 */
#include "stdint.h"
#include "stdio.h"

#include "py/obj.h"
#include "py/runtime.h"

#include "wb-lib/syspublic.h"

// void recordClear(void);
// PositionRecord createPositionRecord(unsigned char x, unsigned char y, unsigned char len, unsigned char size);
// void contentRecordHandle(unsigned char x, unsigned char y, unsigned char len, unsigned char size);
// void OLED_WriteClearPositionRecord(PositionRecord &value);
typedef PositionRecord *PositionRecord_ptr;
typedef PositionRecord_ptr *PositionRecord_ptr_ptr;

mp_obj_t wb_lcd_record_clear(mp_obj_t self_in)
{
    position_record_content_t *self = MP_OBJ_TO_PTR(self_in);

    PositionRecord_ptr q, p = self->head;
    // if (p == NULL)
    //     goto record_clear_ret;

    while (p != NULL)
    {
        q = p;
        p = p->next;
        free(q);
    }
    self->head = NULL;
    // record_clear_ret:
    return mp_const_none; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(wb_lcd_record_clear_obj, wb_lcd_record_clear);

// PositionRecord_ptr 

mp_obj_t wb_lcd_record_check_and_add(size_t n_args, const mp_obj_t *args)
{
    position_record_content_t *self = MP_OBJ_TO_PTR(args[0]); //从第一个参数里面取出对象的指针

    PositionRecord_ptr_ptr p = &(self->head);
    PositionRecord_ptr q = NULL, q_head = NULL, record_last = NULL;
    unsigned char count = 0;

    int start_x = MP_OBJ_SMALL_INT_VALUE(args[1]);
    int start_y = MP_OBJ_SMALL_INT_VALUE(args[2]);
    int end_x = MP_OBJ_SMALL_INT_VALUE(args[3]);
    int end_y = MP_OBJ_SMALL_INT_VALUE(args[4]);

    printf("*p val = %p\n",*p);
    while ((*p) != NULL)
    {
        if (!(((*p)->start_x > end_x) || ((*p)->end_x < start_x) ||
              ((*p)->start_y > end_y) || ((*p)->end_y < start_y)))
        {
            if (q == NULL)
            {
                q_head = *p;
                q = *p;
            }
            else
            {
                q->next = *p;
                q = q->next;
            }
            count++;
            *p = (*p)->next;
        }
        else
        {
            record_last = (*p)->next;
            p = &record_last;
        }
    }
    printf("start malloc\n");
    if (record_last == NULL)
    {
        self->head = malloc(sizeof(PositionRecord));
        record_last = self->head;
    }
    else
    {
        record_last->next = malloc(sizeof(PositionRecord));
        record_last = record_last->next;
    }
    printf("end malloc\n");
    record_last->start_x = start_x;
    record_last->start_y = start_y;
    record_last->end_x = end_x;
    record_last->end_y = end_y;

    // sendACK(mp_obj_get_int(args[1]), mp_obj_get_int(args[2]), bufinfo.buf, bufinfo.len);
    return mp_const_none; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(wb_lcd_record_check_and_add_obj, 5, 5, wb_lcd_record_check_and_add);

mp_obj_t wb_lcd_record_print(mp_obj_t self_in)
{
    position_record_content_t *self = MP_OBJ_TO_PTR(self_in);

    PositionRecord_ptr p = self->head;
    

    while (p != NULL)
    {
        printf("(%d,%d,%d,%d)\n",p->start_x,p->start_y,p->end_x,p->end_y);
        p = p->next;
    }

    return mp_const_none; //返回计算的结果
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(wb_lcd_record_print_obj, wb_lcd_record_print);


//定义type的locals_dict_type
STATIC const mp_rom_map_elem_t position_record_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR_record_clear), MP_ROM_PTR(&wb_lcd_record_clear_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_record_add), MP_ROM_PTR(&wb_lcd_record_check_and_add_obj)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_print), MP_ROM_PTR(&wb_lcd_record_print_obj)},
    // {MP_OBJ_NEW_QSTR(MP_QSTR_get_addr), MP_ROM_PTR(&module_manager_get_addr_obj)},
    // {MP_OBJ_NEW_QSTR(MP_QSTR_get_type_num_buf), MP_ROM_PTR(&module_manager_get_type_num_buf_obj)},
};
//这个定义字典的宏定义
STATIC MP_DEFINE_CONST_DICT(position_record_locals_dict, position_record_locals_dict_table);

const mp_obj_type_t wonderbits_position_record_type;
STATIC mp_obj_t wonderbits_position_record_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args)
{
    mp_arg_check_num(n_args, n_kw, 0, 0, false);                            //检查参数个数
    position_record_content_t *self = m_new_obj(position_record_content_t); //创建对象，分配空间
    self->base.type = &wonderbits_position_record_type;                     //定义对象的类型

    self->head = NULL;

    return MP_OBJ_FROM_PTR(self); //返回对象的指针
}

//定义一个mp_obj_type_t 类型的结构体。注意这里和定义module使用的类型是不一样的
const mp_obj_type_t wonderbits_position_record_type = {
    .base = {&mp_type_type},
    .name = MP_QSTR_PositionRecord, //type 类的name属性是放在这里定义的，而不是放在DICT中
    .make_new = wonderbits_position_record_make_new,
    .locals_dict = (mp_obj_dict_t *)&position_record_locals_dict, //注册math_locals_dict
};

const position_record_content_t mp_const_position_record_obj = {{&wonderbits_position_record_type}, NULL};
