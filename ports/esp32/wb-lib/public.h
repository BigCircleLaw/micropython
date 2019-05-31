#ifndef _WB_PUBLIC_H_
#define _WB_PUBLIC_H_

//  #define WONDERBITS_DEBUG

#define Addr_Master 0x00
#define Addr_Broadcast 0x01
#define Addr_PC 0x02
#define Addr_Error 0x03
#define Addr_Init 0x04

//-------------------//
#define TYPE_INIT 0x00
#define TYPE_RESPONSE 0x01
#define TYPE_INTERRUPT 0x02
#define TYPE_REQUEST 0x03
#define TYPE_REPORT 0x04
//--------------------//
#define TYPE_TEST 0x05
#define TYPE_GETTYPE 0x06
#define TYPE_RETYPE 0x07
#define TYPE_INSERT 0x08
#define TYPE_PULL 0x09


// #define MODULE_TYPE_MAX 0x38

//--------------------//
#define CMD_LED 0x00
#define CMD_ASK_UID 0x01
#define CMD_GET_VERSION 0x02

#ifndef LED_RGB
#define LED_RGB
#define RGB_R 1
#define RGB_G 2
#define RGB_B 3
#define RGB_LB 4
#define RGB_Y 5
#define RGB_P 6
#define RGB_W 7
#define RGB_OFF 8
#endif

#define Master 0x01
#define Slave 0x02

#define IS_FUNCTION_RANG(NUM, MIN, MAX) (((NUM) >= (MIN)) || ((NUM) <= (MAX)))

#endif
