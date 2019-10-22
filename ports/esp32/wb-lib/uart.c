
#include <stdio.h>

#include "driver/uart.h"

#include "wb-lib/hub.h"
#include "wb-lib/uart.h"

// static void wb_uart_irq_handler(void *arg);

void wb_uart_init(void) 
{
    
    uart_config_t uart_config = 
    {
        .baud_rate = 125000,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
    };
    uart_param_config(UART_NUM_2, &uart_config);
    uart_set_pin(UART_NUM_2, 21, 19, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    // uart_driver_install(UART_NUM_2, 2*1024, 0, 0, NULL, 0);
    uart_driver_install(UART_NUM_2, 512, 0, 0, NULL, 0);
    // uart_isr_free(UART_NUM_2);
    // uart_isr_handle_t handle;
    // uart_isr_register(UART_NUM_2, wb_uart_irq_handler, NULL, ESP_INTR_FLAG_LOWMED | ESP_INTR_FLAG_IRAM, &handle);
    // uart_enable_rx_intr(UART_NUM_2);
    // uart_set_rx_timeout(UART_NUM_2, 10);
}

// all code executed in ISR must be in IRAM, and any const data must be in DRAM
// static void IRAM_ATTR wb_uart_irq_handler(void *arg) 
// {
//     volatile uart_dev_t *uart = &UART1;
//     // UART1_SendByte(0x00);
//     uart->int_clr.rxfifo_full = 1;
//     uart->int_clr.frm_err = 1;
//     uart->int_clr.rxfifo_tout = 1;

//     while (uart->status.rxfifo_cnt) 
//     {

//         uint8_t c = uart->fifo.rw_byte;
//         hub_put(c);
        
//     }
// }

void Uart_send(unsigned char *data, unsigned char len)
{
    uart_write_bytes(UART_NUM_2, (const char*)data, len);
}

void UART1_SendByte(unsigned char data)
{
    uart_write_bytes(UART_NUM_2, (const char*)&data, 1);
}
