
#include "mpconfigport.h"

#include "wb-lib/receiver.h"
#include "wb-lib/public.h"
#include "wb-lib/module_manager.h"
#include "wb-lib/tool.h"

bool translate_check(unsigned char *buf)
{
    struct Head *h = (struct Head *)(buf + 1);
    unsigned char hbase = sizeof(struct Head) + 1;
    if (MSG_START_TAG != buf[0])
        return 0;
    if (!(SysAddr == h->targetAdd || Addr_Broadcast == h->targetAdd))
        return 0;
    if (h->length > (MSG_END_TAG - 7))
        return 0;
    // UART1_SendByte(h->sourceAdd);
    if (((h->sourceAdd < 0x10) || (h->sourceAdd >= module_manager_base_addr)) && (h->sourceAdd != Addr_Init) && (h->sourceAdd != Addr_PC))
        return 0;

    unsigned char chr[4];
    unsigned char DataBuffer;
    unsigned char i, j;
    for (i = h->length, j = 0; (*(buf + hbase + i) != MSG_END_TAG) && (i < MSG_MAX_LENGTH_ALL);)
    {
        DataBuffer = *(buf + hbase + i++);
        if (DataBuffer == MSG_TRANSLATE_TAG)
            DataBuffer += *(buf + hbase + i++);
        chr[j++] = DataBuffer;
        if (j >= 4)
            break;
    }
    *(buf + h->length + hbase) = chr[0];
    *(buf + h->length + hbase + 1) = chr[1];


    bool state = CRC16Bit(buf, h->length + hbase + 2) == 0;
    // UART1_SendByte((unsigned char)state);
    unsigned char index = 0;
    hbase = hbase + h->length;

    for (i = 1; (i < (hbase)) && (i < MSG_MAX_LENGTH_ALL);)
    {
        DataBuffer = *(buf + i++);
        if (DataBuffer == MSG_TRANSLATE_TAG)
            DataBuffer += *(buf + i++); //Combine the value that have been broke up(0xFD, 0xFE and 0xFF)
        buf[index++] = DataBuffer;
        // UART1_SendByte(DataBuffer);
    }

    h = (struct Head *)buf;
    h->length = index - sizeof(struct Head);

    return state;
}
