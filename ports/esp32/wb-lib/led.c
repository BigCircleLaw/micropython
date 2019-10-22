
#include "driver/gpio.h"

#include "wb-lib/public.h"

#define GPIO_OUTPUT_RED_IO 32
#define GPIO_OUTPUT_GREEN_IO 33
#define GPIO_OUTPUT_BLUE_IO 27
#define GPIO_OUTPUT_PIN_SEL ((1ULL << GPIO_OUTPUT_RED_IO) | (1ULL << GPIO_OUTPUT_GREEN_IO) | (1ULL << GPIO_OUTPUT_BLUE_IO))

void led_set_color(unsigned char val)
{
    // if (RGB_R == val)
    // {
    //     gpio_set_level(GPIO_OUTPUT_RED_IO, 0);
    //     gpio_set_level(GPIO_OUTPUT_GREEN_IO, 1);
    //     gpio_set_level(GPIO_OUTPUT_BLUE_IO, 1);
    // }
    // else if (RGB_G == val)
    // {
    //     gpio_set_level(GPIO_OUTPUT_RED_IO, 1);
    //     gpio_set_level(GPIO_OUTPUT_GREEN_IO, 0);
    //     gpio_set_level(GPIO_OUTPUT_BLUE_IO, 1);
    // }
    // else if (RGB_B == val)
    // {
    //     gpio_set_level(GPIO_OUTPUT_RED_IO, 1);
    //     gpio_set_level(GPIO_OUTPUT_GREEN_IO, 1);
    //     gpio_set_level(GPIO_OUTPUT_BLUE_IO, 0);
    // }
    // else if (RGB_LB == val)
    // {
    //     gpio_set_level(GPIO_OUTPUT_RED_IO, 1);
    //     gpio_set_level(GPIO_OUTPUT_GREEN_IO, 0);
    //     gpio_set_level(GPIO_OUTPUT_BLUE_IO, 0);
    // }
    // else if (RGB_Y == val)
    // {
    //     gpio_set_level(GPIO_OUTPUT_RED_IO, 0);
    //     gpio_set_level(GPIO_OUTPUT_GREEN_IO, 0);
    //     gpio_set_level(GPIO_OUTPUT_BLUE_IO, 1);
    // }
    // else if (RGB_P == val)
    // {
    //     gpio_set_level(GPIO_OUTPUT_RED_IO, 0);
    //     gpio_set_level(GPIO_OUTPUT_GREEN_IO, 1);
    //     gpio_set_level(GPIO_OUTPUT_BLUE_IO, 0);
    // }
    // else if (RGB_W == val)
    // {
    //     gpio_set_level(GPIO_OUTPUT_RED_IO, 0);
    //     gpio_set_level(GPIO_OUTPUT_GREEN_IO, 0);
    //     gpio_set_level(GPIO_OUTPUT_BLUE_IO, 0);
    // }
    // else 
    // {
    //     gpio_set_level(GPIO_OUTPUT_RED_IO, 1);
    //     gpio_set_level(GPIO_OUTPUT_GREEN_IO, 1);
    //     gpio_set_level(GPIO_OUTPUT_BLUE_IO, 1);
    // }
}

void led_init(void)
{
    // gpio_config_t io_conf;
    // //disable interrupt
    // io_conf.intr_type = GPIO_PIN_INTR_DISABLE;
    // //set as output mode
    // io_conf.mode = GPIO_MODE_OUTPUT;
    // //bit mask of the pins that you want to set,e.g.GPIO18/19
    // io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
    // //disable pull-down mode
    // io_conf.pull_down_en = 1;
    // //disable pull-up mode
    // io_conf.pull_up_en = 1;
    // //configure GPIO with the given settings
    // gpio_config(&io_conf);

    // led_set_color(RGB_OFF);
}
