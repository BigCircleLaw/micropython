from machine import Timer
import wb
# from framehub import distribute
import framehub
import time
from ModuleManager import moduleManager as mMag

tim_hub = Timer(1)

tim_hub.init(period=30, mode=Timer.PERIODIC, callback=framehub.distribute)

wb.init()

wb.module_manager.start()


_module_info = []

time.sleep_ms(10)
framehub.flag = True
time.sleep_ms(10)
# mMag.doUpdate()

wb.led.blue()

del mMag
del Timer
del wb
del framehub
del time

def getModuleInformation():
    return _module_info
