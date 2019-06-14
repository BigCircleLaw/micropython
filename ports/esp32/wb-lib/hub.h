#ifndef _WB_HUB_H_
#define _WB_HUB_H_


void  hub_put(unsigned char data);
unsigned char * hub_distribute(void);
unsigned char hub_available(void);

void response_cache_set(unsigned char addr, unsigned char *data);
unsigned char *response_cache_get(unsigned char addr);

void hub_init(void);

#endif
