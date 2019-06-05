
#include "mpconfigport.h"

#include "wb-lib/public.h"
#include "wb-lib/receiver.h"
#include "wb-lib/module_manager.h"

#include "wb-lib/uart.h"

#define HUB_MAX 10

static unsigned char buf[HUB_MAX][MSG_MAX_LENGTH_ALL];
static unsigned char index = 0;
static unsigned char head = 0;
static unsigned char tail = 0;
static unsigned char num = 0;




void  hub_put(unsigned char data)
{
    
    if (MSG_START_TAG == data)
    {
        index = 0;
    }

    buf[head][index++] = data;
    if (index > MSG_MAX_LENGTH_ALL)
        index = MSG_MAX_LENGTH_ALL - 1;
    if ((MSG_END_TAG != data) || ((index) < 8))
        return;

    index = 0;
    if (translate_check(buf[head]))
    {
        // (buf.buf + 1);
        // struct Head *head = (struct Head *)data;

        if (num >= HUB_MAX)
            return; //�
        num++;
        head = (head + 1) % HUB_MAX;

    }
}

void hub_distribute(void)
{
    // UART1_SendByte(num);
    while(num > 0)
    {
        struct Head *head = (struct Head *)buf[tail];
        unsigned char *content = buf[tail] + sizeof(struct Head);
        
        // UART1_SendByte(head->length);
        // Uart_send(buf[tail], head->length + 4);
        
        // UART1_SendByte(0xF0);
        // UART1_SendByte(head->type);
        switch (head->type)
        {

        case TYPE_INIT:
            module_manager_put(content, head->length);
            break;
        case TYPE_RESPONSE:
            // this->setResponseID(head->sourceAdd, tail);
            break;
        case TYPE_REPORT:
            // module_manager_doReport(head->sourceAdd, buf[tail]);
            break;
        case TYPE_INSERT:
            // if (head->length == 1)
            // {
            //     if (content[0] >= MODULE_TYPE_MAX)
            //         return;
            // }
            // ESP.restart();
            break;
            
        }
        // UART1_SendByte(0);

        tail = (tail + 1) % HUB_MAX;
        num--;
    }
}
