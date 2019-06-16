
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
    // UART1_SendByte(0xF0);
    // UART1_SendByte(num);
    return num; 
}

#define HUB_RESPONSE_MAX 10

static unsigned char response_cache_addr[HUB_RESPONSE_MAX];
static unsigned char response_cache_buf[HUB_RESPONSE_MAX][MSG_MAX_LENGTH_ALL];
static unsigned char response_cache_index = 0;

void response_cache_set(unsigned char addr, unsigned char *data)
{
    response_cache_addr[response_cache_index] = addr;
    
    unsigned char len = data[3] + 4;
    for(unsigned char i = 0; i < len; i++)
    {
        response_cache_buf[response_cache_index][i] = data[i];
    }

    response_cache_index = (response_cache_index + 1) % HUB_RESPONSE_MAX;
}
unsigned char *response_cache_get(unsigned char addr)
{
    for(unsigned char i = 0; i < HUB_RESPONSE_MAX; i++)
    {
        if(addr == response_cache_addr[i])
        {
            response_cache_addr[i] = Addr_Error;
            return response_cache_buf[i];
        }
    }
    return NULL;
}

void hub_init(void)
{
    index = 0;
    head = 0;
    tail = 0;
    num = 0;
    response_cache_index = 0;
    for(unsigned char i = 0; i < HUB_RESPONSE_MAX; i++)
        response_cache_addr[i] = Addr_Error;
}
