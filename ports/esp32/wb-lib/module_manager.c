
#include "stdio.h"

#include "py/obj.h"
#include "py/mphal.h"
#include "py/misc.h"

#include "wb-lib/public.h"
#include "wb-lib/module_manager.h"
#include "wb-lib/sender.h"
#include "wb-lib/led.h"
#include "wb-lib/tool.h"
#include "wb-lib/uart.h"

#include "wb-lib/syspublic.h"

// typedef struct LinkList
// {
//     module_obj_content_t *head;
//     module_obj_content_t *tail;
// } LinkList;

unsigned char module_manager_base_addr = 1; //地址分配时地址计数

static unsigned char bufSendLen; //在初始化阶段用来记录从机UID长度，之后用来表示bufSend长度

// static TypeStorage *definedModuleTypeNum = NULL;  //该种类在程序中定义的数量
// static unsigned char definedModuleType_count = 0; //所有定义模块的地址数量
// static LinkList definedModuleLinkList = {NULL, NULL}; //该种类在程序中定义组成的链表

static TypeStorage *num = NULL;      //该种类连接在主机上的数量
static Module *listHead = NULL;      //listqueue的头地址
static Module *listqueue = NULL;     //记录从机发上来的类型，UID。
static ModuleStorage *list = NULL;   //对应类型存下UID
static AddrStorage *addrData = NULL; //所有模块的地址存储这里
static unsigned char addr_count = 0; //所有模块的地址数量
// static unsigned char type_buf[0] = 0; //所有模块的类型数量

static unsigned char type_buf[200];

unsigned char *module_manager_sendTypeAddrtoPC(void)
{
#if WONDERBITS_DEBUG
    printf("module_manager_sendTypeAddrtoPC\n");
    printf("type_buf[0]: %d,", type_buf[0]);
    for (unsigned char i = 0; i < type_buf[0]; i++)
    {
        printf("type: %d,", num[i].type);
        printf("num: %d,", num[i].num);
    }
    printf("\n");
#endif
    return type_buf;
}

unsigned char module_manager_getAddr(unsigned char id, unsigned char type)
{
#if WONDERBITS_DEBUG
    printf("module_manager_getAddr\n");
    printf("type: %d, id: %d\n", type, id);
    printf("type_buf[0]: %d\n", type_buf[0]);
#endif
    unsigned char addrCount = 0;
    for (unsigned char i_type = 0; i_type < type_buf[0]; i_type++)
    {
#if WONDERBITS_DEBUG
        printf("type: %d, num: %d\n", num[i_type].type, num[i_type].num);
#endif
        if ((type == num[i_type].type) && (id <= num[i_type].num))
        {
#if WONDERBITS_DEBUG
            printf("addr: %d\n", addrData[addrCount + id].addr);
#endif
            // addrData[addrCount + id - 1].flag = 1;
            return addrData[addrCount + id].addr;
        }
        addrCount += num[i_type].num;
    }
    return Addr_Error;
}

int ModuleComp(const void *a, const void *b)
{
    int i = 0;
    ModuleStorage *p_a = (ModuleStorage *)a;
    ModuleStorage *p_b = (ModuleStorage *)b;
    // unsigned char lengthValue = bufSendLen;
    for (i = 0; i < bufSendLen; i++)
    {
        if (p_a->uid[i] == p_b->uid[i])
            continue;
        else
            return p_a->uid[i] - p_b->uid[i];
    }
    return 0;
}

void module_manager_put(unsigned char *uid, unsigned char len)
{
    // UART1_SendByte(0xF2);
    module_manager_base_addr = 1;
    if (listHead == NULL)
    {
        // UART1_SendByte(0x13);
        listHead = m_new(Module, 1);
        if (NULL == listHead)
            return;
        listqueue = listHead;
        listqueue->next = NULL;
        // UART1_SendByte(0xF3);
    }
    else
    {
        // UART1_SendByte(0x14);
        listqueue->next = m_new(Module, 1);
        if (NULL == listqueue->next)
            return;
        listqueue = listqueue->next;
        listqueue->next = NULL;
        // UART1_SendByte(0xF4);
    }
    // UART1_SendByte(len);
    if (len > bufSendLen)
        bufSendLen = len;
    listqueue->uid = m_new(unsigned char, len);
    ustrncpy(listqueue->uid, uid, len); //保留类型的原因是要使用到排序中

    // Uart_send(uid, len);
    // Uart_send(listqueue->uid, len);

    addr_count++;
    // UART1_SendByte(addr_count);
}

void module_manager_getlist(void)
{
    list = m_new(ModuleStorage, addr_count);
    if (NULL == list)
        return;
    // UART1_SendByte(addr_count);

    if (addr_count <= 0)
        return;
    int j = 0;
    listqueue = listHead;

    while (listqueue != NULL)
    {
        list[j].uid = listqueue->uid;

        listqueue = listqueue->next;

        listHead->uid = NULL;
        m_free(listHead);
        listHead = listqueue;
        j++;
    }
    num = (TypeStorage *)&type_buf[1];
    int i = 0;
    for (i = 0; i < addr_count; i++)
    {
        num[i].type = 0xFF;
        // num[i].num = 0;
    }
    num[0].type = list[0].uid[0];
    num[0].num = 1;
    type_buf[0] = 1;
    // UART1_SendByte(num[0].type);
    // for (i = 1; i < addr_count; i++)
    // {
    //     unsigned char type_val = list[i].uid[0];
    //     // UART1_SendByte(type_val);

    //     for (j = i - 1; (j >= 0) && (type_val < num[j].type); j--)
    //     {
    //         num[j + 1] = num[j];
    //     }
    //     if ((type_val == num[j].type) && (j >= 0))
    //     {
    //         num[j].num++;
    //     }
    //     else
    //     {
    //         num[j + 1].type = type_val;
    //         num[j + 1].num = 1;
    //         type_buf[0]++;
    //     }
    // }
    for (i = 1; i < addr_count; i++)
    {
        unsigned char type_val = list[i].uid[0], current_type;

        for (j = 0; (j < type_buf[0]); j++)
        {
            if (type_val < (current_type = num[j].type))
            {
                for (unsigned char k = type_buf[0]; k > j; k--)
                {
                    num[k] = num[k - 1];
                }
                num[j].type = type_val;
                num[j].num = 1;
                type_buf[0]++;
                break;
            }
            if (type_val == current_type)
            {
                num[j].num++;
                break;
            }
            // num[j + 1] = num[j];
        }
        if (j >= type_buf[0])
        {
            // if ((type_val > current_type))
            {
                num[j].type = type_val;
                num[j].num = 1;
                type_buf[0]++;
            }
        }
    }
}

void module_manager_sort(void)
{
    qsort(list, addr_count, sizeof(ModuleStorage), ModuleComp);
}

/**
    @brief  ��   
    @param  None
    @retval None
*/
void module_manager_sendID(void)
{
    //  const unsigned char sendID_Len = 14;
    int i, j = 0, i_type = 0, j_num = 0;
    unsigned char data[bufSendLen + 1];
    // UART1_SendByte(type_buf[0]);
    for (i_type = 0; i_type < type_buf[0]; i_type++)
    {
        // UART1_SendByte(num[i_type].type);
        // UART1_SendByte(num[i_type].num);
        for (j_num = 0; j_num < num[i_type].num; j_num++)
        {
            data[0] = addrData[j].addr;
            // if (addrData[j].flag == 1)
            // {
            data[1] = RGB_B;
            // }
            // else
            // {
            //     data[1] = RGB_LB;
            // }
            for (i = 1; i < bufSendLen; i++)
            {
                data[1 + i] = list[j].uid[i];
            }
            sendACK(Addr_Broadcast, TYPE_RESPONSE, data, bufSendLen + 1);
            mp_hal_delay_ms(2);
            m_free(list[j].uid);
            list[j].uid = NULL;
            j += 1;
        }
    }
    m_free(list);
    list = NULL;
    bufSendLen = 0;
}

void module_manager_loadID(void)
{
    unsigned char j_num = 0;
    addrData = (AddrStorage *)&type_buf[type_buf[0] * 2 + 1];
    if (NULL == addrData)
        return;
    module_manager_base_addr = MODULE_ADDR_Start;
    for (j_num = 0; j_num < addr_count; j_num++)
    {
        addrData[j_num].addr = module_manager_base_addr++;
        addrData[j_num].flag = 0;
        // mp_hal_delay_ms(1);
    }
    module_manager_sendID();
}

void module_manager_init(void)
{
    unsigned char i;
    unsigned char cmd = CMD_ASK_UID;
//init...
#if WONDERBITS_DEBUG
    printf("module_manager_init\n");
#endif
    num = NULL;       //该种类连接在主机上的数量
    listHead = NULL;  //listqueue的头地址
    listqueue = NULL; //记录从机发上来的类型，UID。
    list = NULL;      //对应类型存下UID
    addrData = NULL;
    addr_count = 0;
    type_buf[0] = 0;
    // mp_hal_delay_ms(100);
    led_set_color(RGB_R);
    sendACK(Addr_Broadcast, TYPE_INIT, &cmd, 1);

    for (i = 0; (i < 3) || (module_manager_base_addr == 1); i++)
    {
        module_manager_base_addr = 0;
        led_set_color(RGB_Y);
        mp_hal_delay_ms(50);
        led_set_color(RGB_OFF);
        mp_hal_delay_ms(50);
    }

    led_set_color(RGB_LB);
#if WONDERBITS_DEBUG
    printf("module_manager_put finished\n");
#endif
    module_manager_getlist();
#if WONDERBITS_DEBUG
    printf("module_manager_getlist finished\n");
#endif
    module_manager_sort();
#if WONDERBITS_DEBUG
    printf("module_manager_sort finished\n");
#endif
    module_manager_loadID();
#if WONDERBITS_DEBUG
    printf("module_manager_loadID finished\n");
#endif

    // configurationVersion();
}
