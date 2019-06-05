#ifndef _WB_UART_H_
#define _WB_UART_H_


void wb_uart_init(void);
void Uart_send(unsigned char *data, unsigned char len);
void UART1_SendByte(unsigned char data);


#endif
