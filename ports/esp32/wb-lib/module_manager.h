#ifndef _WB_MODULE_MANAGER_H_
#define _WB_MODULE_MANAGER_H_

// #define MODULE_Macaddr_len 12

typedef struct _Module //做链表
{
  //  unsigned char uidLen;
  unsigned char *uid;
  struct _Module *next;
}Module;
typedef struct _TypeStorage
{
  unsigned char type;
  unsigned char num;
}TypeStorage;
typedef struct AddrStorage
{
  unsigned char addr:7;
  unsigned char flag:1;
} AddrStorage;
#define _INQUiRE_WHETHER_ONLINE_ 0x01
#define _ONLINE_FLAG_ 0x02

typedef struct _ModuleStorage //
{
  unsigned char *uid;
}ModuleStorage;


extern unsigned char module_manager_base_addr;


void module_manager_put(unsigned char *uid, unsigned char len);
void module_manager_init(void);
unsigned char module_manager_getAddr(unsigned char id, unsigned char type);
unsigned char *module_manager_sendTypeAddrtoPC(void);



#endif
