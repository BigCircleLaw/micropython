#ifndef UTF8_2_GB2312_H_INCLUDED
#define UTF8_2_GB2312_H_INCLUDED

typedef unsigned char u8;
typedef unsigned short int u16;


int Utf8ToGb2312(const char* utf8, int len,u8* gbArray);

#endif // UTF8_2_GB2312_H_INCLUDED
