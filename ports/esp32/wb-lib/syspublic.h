#ifndef _WB_SYSPUBLIC_H_
#define _WB_SYSPUBLIC_H_

#include "public.h"

#define SysAddr Addr_Master //系统地址

#define MSG_MAX_LENGTH_ALL 45 //消息包最大长度，不是内容长度

#define MSG_START_TAG 0xFF
#define MSG_END_TAG 0xFE
#define MSG_TRANSLATE_TAG 0xFD //转义字符

// #define LEDOUTPUT     \
//   pinMode(5, OUTPUT); \
//   pinMode(2, OUTPUT); \
//   pinMode(23, OUTPUT);
// #define _Red_()          \
//   digitalWrite(5, LOW);  \
//   digitalWrite(2, HIGH); \
//   digitalWrite(23, HIGH);
// #define _Green_()        \
//   digitalWrite(5, HIGH);  \
//   digitalWrite(2, LOW); \
//   digitalWrite(23, HIGH);
// #define _Blue_()         \
//   digitalWrite(5, HIGH);  \
//   digitalWrite(2, HIGH); \
//   digitalWrite(23, LOW);
// #define _Yellow_()       \
//   digitalWrite(5, LOW);  \
//   digitalWrite(2, LOW); \
//   digitalWrite(23, HIGH);
// #define _LBlue_()        \
//   digitalWrite(5, HIGH);  \
//   digitalWrite(2, LOW); \
//   digitalWrite(23, LOW);
// #define _Purple_()       \
//   digitalWrite(5, LOW);  \
//   digitalWrite(2, HIGH); \
//   digitalWrite(23, LOW);
// #define _White_()        \
//   digitalWrite(5, LOW);  \
//   digitalWrite(2, LOW); \
//   digitalWrite(23, LOW);
// #define _None_()         \
//   digitalWrite(5, HIGH);  \
//   digitalWrite(2, HIGH); \
//   digitalWrite(23, HIGH);


struct Head //消息包头
{
  unsigned char targetAdd; //目标地址
  unsigned char sourceAdd; //源地址
  unsigned char type;      //消息类型
  unsigned char length;    //内容长度
};

struct Tail
{
  unsigned char crcH; //CRC的高8位
  unsigned char crcL; //CRC的低8位
};

struct Message
{
  struct Head head;
  unsigned char *data;
};

struct stPackage
{
  unsigned char startTag; //起始标志位 0XFF
  struct Head head;
  unsigned char *data;
  struct Tail tail;
  unsigned char endTag; //结束标志位 0XFE
};

struct ReceiveData
{
  unsigned char buf[MSG_MAX_LENGTH_ALL];
  unsigned char index;
};

#endif
