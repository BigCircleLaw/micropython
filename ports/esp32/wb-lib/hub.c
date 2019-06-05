
#include "mpconfigport.h"

#include "wb-lib/public.h"
#include "wb-lib/receiver.h"

#define HUB_MAX 4

void  hub_put(unsigned char data)
{
    
    // if (MSG_START_TAG == data)
    // {
    //     this->index = 0;
    // }

    // this->buf[this->head][this->index++] = data;
    // if (this->index > MSG_MAX_LENGTH_ALL)
    //     this->index = MSG_MAX_LENGTH_ALL - 1;
    // if ((MSG_END_TAG != data) || ((this->index) < 8))
    //     return;

    // this->index = 0;
    // if (translate_check(this->buf[this->head]))
    // {
    //     // (this->buf.buf + 1);

    //     // struct Head *head = (struct Head *)data;

    //     if (this->num >= HUB_MAX)
    //         return; //�
    //     this->num++;
    //     this->head++;

    //     if (HUB_MAX == this->head)
    //         this->head = 0;
    // }
}
