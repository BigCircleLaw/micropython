
#include "wb-lib/uart.h"
#include "wb-lib/public.h"
#include "wb-lib/tool.h"

unsigned char Sender_send(Message *msg, unsigned char *buf)
{
    unsigned char len = msg->head.length;
    unsigned char *p = msg->data;
    unsigned char index;

    //将头填充,下面加1由于buf的第0字节是起始0xFF
    buf[0] = MSG_START_TAG;
    buf[1] = msg->head.targetAdd;
    buf[2] = msg->head.sourceAdd;
    buf[3] = msg->head.type;

    index = sizeof(struct Head) + 1;

    //将数据放入发送缓存区
    while (len--)
    {
        // saveToBuffer(*p++);

        if (*p >= 0xFD)
        { //FF FE FD
            /*  0xFF    --->      0xFD, 0x02
            0xFE    --->      0xFD, 0x01
            0xFD    --->      0xFD, 0x00  */
            buf[index++] = 0xFD;
            buf[index++] = *p - 0xFD;
        }
        else
        {
            buf[index++] = *p;
        }
        p++;
    }

    buf[4] = index - (sizeof(struct Head) + 1); //计算长度，不包括crc长度

    unsigned int CRC; //CRC

    CRC = CRC16Bit(buf, index);

    // saveToBuffer((CRC / 256)); //CRC Higher byte
    // saveToBuffer((CRC % 256)); //CRC Lower byte

    len = CRC / 256;
    if (len >= 0xFD)
    { //FF FE FD
        /*  0xFF    --->      0xFD, 0x02
            0xFE    --->      0xFD, 0x01
            0xFD    --->      0xFD, 0x00  */
        buf[index++] = 0xFD;
        buf[index++] = len - 0xFD;
    }
    else
    {
        buf[index++] = len;
    }
    len = CRC % 256;
    if (len >= 0xFD)
    { //FF FE FD
        /*  0xFF    --->      0xFD, 0x02
            0xFE    --->      0xFD, 0x01
            0xFD    --->      0xFD, 0x00  */
        buf[index++] = 0xFD;
        buf[index++] = len - 0xFD;
    }
    else
    {
        buf[index++] = len;
    }

    buf[index++] = MSG_END_TAG;
    return index;
}

static unsigned char moduleSendBuf[MSG_MAX_LENGTH_ALL];
void sendACK(unsigned char addrValue, unsigned char type, unsigned char *data, unsigned char len)
{
    
    struct Message msg;
    msg.head.targetAdd = addrValue;
    msg.head.sourceAdd = Addr_Master;
    msg.head.type = type;
    msg.head.length = len;
    msg.data = data;
    unsigned char send_len = Sender_send(&msg, moduleSendBuf);
    Uart_send(moduleSendBuf, send_len);
}
