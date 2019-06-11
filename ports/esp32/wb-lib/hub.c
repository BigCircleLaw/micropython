
#include "mpconfigport.h"

#include "wb-lib/public.h"
#include "wb-lib/receiver.h"
#include "wb-lib/module_manager.h"

#include "wb-lib/uart.h"

#define HUB_MAX 30

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

unsigned char * hub_distribute(void)
{
    // UART1_SendByte(num);
    if(num > 0)
    {
        // struct Head *head = (struct Head *)buf[tail];
        // unsigned char *content = buf[tail] + sizeof(struct Head);

        unsigned char *content = buf[tail];

        tail = (tail + 1) % HUB_MAX;
        num--;
        return content;
    }
    return NULL;
}

unsigned char hub_available(void)
{
   return num; 
}
