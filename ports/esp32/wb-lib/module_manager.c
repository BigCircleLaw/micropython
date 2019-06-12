
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
static unsigned char type_count = 0; //所有模块的类型数量


unsigned char *module_manager_sendTypeAddrtoPC(void)
{
    #if WONDERBITS_DEBUG
    printf("module_manager_sendTypeAddrtoPC\n");
    printf("type_count: %d,", type_count);
    #endif
    unsigned char i;
    unsigned char *sendPCBuffer = m_new(unsigned char, type_count * 2 + 1);
    if(sendPCBuffer == NULL)
        return NULL;
    unsigned char position = 0;
    sendPCBuffer[position++] = type_count;
    for (i = 0; i < type_count; i++)
    {
        sendPCBuffer[position++] = num[i].type;
        sendPCBuffer[position++] = num[i].num;
        #if WONDERBITS_DEBUG
        printf("type: %d,", num[i].type);
        printf("num: %d,", num[i].num);
        #endif
    }
    #if WONDERBITS_DEBUG
    printf("\n");
    #endif
    return sendPCBuffer;
}

unsigned char module_manager_getAddr(unsigned char id, unsigned char type)
{
#if WONDERBITS_DEBUG
    printf("module_manager_getAddr\n");
    printf("type: %d, id: %d\n", type, id);
    printf("type_count: %d\n", type_count);
#endif
    unsigned char addrCount = 0;
    for (unsigned char i_type = 0; i_type < type_count; i_type++)
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
}

void module_manager_getlist(void)
{
    unsigned char i;
    unsigned char typeNum[MODULE_TYPE_MAX];
    // UART1_SendByte(MODULE_TYPE_MAX);
    for (i = 0; i < MODULE_TYPE_MAX; i++)
    {
        typeNum[i] = 0;
    }
    listqueue = listHead;
    while (listqueue != NULL)
    {
        typeNum[listqueue->uid[0]] += 1;
        // UART1_SendByte(listqueue->uid[0]);
        listqueue = listqueue->next;
    }
    for (i = 0; i < MODULE_TYPE_MAX; i++)
    {
        if (typeNum[i] != 0)
        {
            type_count += 1;
        }
    }
    // UART1_SendByte(type_count);
    num = m_new(TypeStorage, type_count);
    unsigned char j = 0;
    for (i = 0; i < MODULE_TYPE_MAX; i++)
    {
        if (typeNum[i] != 0)
        {
            num[j].type = i;
            num[j].num = typeNum[i];
            // UART1_SendByte(i);
            // UART1_SendByte(typeNum[i]);
            j += 1;
        }
    }
    ////////////////////////////////////////////////////////////////////////
    // j = 0;
    // for (i = 0; i < MODULE_TYPE_MAX; i++)
    // {
    //     typeNum[i] = 0;
    // }

    // definedModuleLinkList.tail = definedModuleLinkList.head;
    // while (definedModuleLinkList.tail != NULL)
    // {
    //     typeNum[definedModuleLinkList.tail->type] += 1;
    //     definedModuleLinkList.tail = definedModuleLinkList.tail->next;
    // }
    /********************************************************************************************/
    //计算用户定义的每种类型模块的数量
    // for (i = 0; i < MODULE_TYPE_MAX; i++)
    // {
    //   if (typeNum[i] != 0)
    //   {
    //     definedModuleType_count += 1;
    //   }
    // }
    // definedModuleTypeNum = new TypeStorage[definedModuleType_count];

    // for (i = 0; i < MODULE_TYPE_MAX; i++)
    // {
    //   if (typeNum[i] != 0)
    //   {
    //     definedModuleTypeNum[j].type = i;
    //     definedModuleTypeNum[j].num = typeNum[i];
    //     j += 1;
    //   }
    // }
    /********************************************************************************************/
    ///////////////////////////////////////////////////////////////////////
    list = m_new(ModuleStorage, addr_count);
    if (NULL == list)
        return;
    // UART1_SendByte(addr_count);
    j = 0;
    listqueue = listHead;

    while (listqueue != NULL)
    {
        list[j].uid = m_new(unsigned char, bufSendLen);
        // if (list[j].uid == NULL)
        //   return;

        ustrncpy(list[j].uid, listqueue->uid, bufSendLen);
        //      UART1_SendByte(j);
        listqueue = listqueue->next;
        m_free(listHead->uid);
        listHead->uid = NULL;
        m_free(listHead);
        listHead = listqueue;
        j++;
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
    //  UART1_SendByte(num[i_type]);
    for (i_type = 0; i_type < type_count; i_type++)
    {
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
    addrData = m_new(AddrStorage, addr_count);
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

    // mp_hal_delay_ms(100);
    led_set_color(RGB_OFF);
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
    module_manager_getlist();
    module_manager_sort();
    module_manager_loadID();

    // configurationVersion();
}

void module_manager_doReport(unsigned char id, unsigned char *data)
{
    // definedModuleLinkList.tail = definedModuleLinkList.head;
    // while (definedModuleLinkList.tail != NULL)
    // {
    //     if (definedModuleLinkList.tail->des_addr == id)
    //     {
    //         // definedModuleLinkList.tail->getData(data);
    //         return; //
    //     }
    //     definedModuleLinkList.tail = definedModuleLinkList.tail->next;
    // }
}
void module_manager_doUpdate(void)
{
    // definedModuleLinkList.tail = definedModuleLinkList.head;
    // while (definedModuleLinkList.tail != NULL)
    // {
    //     // definedModuleLinkList.tail->doUpdateValue();
    //     definedModuleLinkList.tail = definedModuleLinkList.tail->next;
    // }
}

unsigned char module_manager_getSendBufLength(void)
{
    return bufSendLen;
}
