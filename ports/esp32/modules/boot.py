import time
from machine import reset
print(time.ticks_ms())
import system
import gc

print(time.ticks_ms())
# from sysCfg import *

print(time.ticks_ms())
# import machine, time
# from connectWeb import webrepl_start
# from system import sysInit, getModuleInformation
# from wb_sys import *

from public import RGB_R, RGB_B, RGB_G, RGB_LB, RGB_OFF, RGB_P, RGB_W, RGB_Y

from EventManager import event

gc.collect()
del gc
