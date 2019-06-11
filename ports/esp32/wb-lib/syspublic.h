#ifndef _WB_SYSPUBLIC_H_
#define _WB_SYSPUBLIC_H_

typedef struct _module_manager_content_t
{
    mp_obj_base_t base;   //定义的对象结构体要包含该成员
    
}module_manager_content_t;

typedef struct _frame_hub_content_t
{
    mp_obj_base_t base;   //定义的对象结构体要包含该成员

}frame_hub_content_t;

typedef struct _led_control_content_t
{
    mp_obj_base_t base;   //定义的对象结构体要包含该成员
    unsigned char color;

}led_control_content_t;


#endif
