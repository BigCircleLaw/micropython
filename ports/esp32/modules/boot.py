# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
# esp.osdebug(None)
# import webrepl
# import network
# from machine import Pin
# from wb_sys import *

# sta_if = network.WLAN(network.STA_IF);
# sta_if.active(True)
# sta_if.connect("MFE", "MF3ducati0n")
# while not sta_if.isconnected():
#     pass
# print('wifi connected.')
# webrepl.start()

# sysInit()

# sta_if.connect("Stefan_computer", "1234568790")
import time
from machine import reset
print(time.ticks_ms())
import system

print(time.ticks_ms())
from sysCfg import *

print(time.ticks_ms())
# import machine, time
# from connectWeb import webrepl_start
# from system import sysInit, getModuleInformation
# from wb_sys import *

from public import RGB_R, RGB_B, RGB_G, RGB_LB, RGB_OFF, RGB_P, RGB_W, RGB_Y

from EventManager import event
