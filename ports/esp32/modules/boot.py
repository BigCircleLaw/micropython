import time
from machine import reset
print(time.ticks_ms())
import system
import os
import gc

print(time.ticks_ms())
if 'main.py' not in os.listdir():
    exec('from wonderbits import *')

print(time.ticks_ms())

from public import RGB_R, RGB_B, RGB_G, RGB_LB, RGB_OFF, RGB_P, RGB_W, RGB_Y

del os
gc.collect()

del gc
time.sleep_ms(200)

# import _thread
# import wb

# def event_task_run(val):
#     while True:
#         wb.send_a_data(val)
#         wb.task_switch_then_back()


# _thread.start_new_thread(event_task_run, (0x00,))
# _thread.start_new_thread(event_task_run, (0x01,))

# def event_task_run():
#     while True:
#         wb.send_a_data(0)
#         wb.task_switch_then_back()


# _thread.start_new_thread(event_task_run, ())

# def event_task_run1():
#     while True:
#         wb.send_a_data(1)
#         wb.task_switch_then_back()
# _thread.start_new_thread(event_task_run1, ())
