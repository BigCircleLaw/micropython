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

from EventManager import event

del os
gc.collect()

del gc
time.sleep_ms(200)
