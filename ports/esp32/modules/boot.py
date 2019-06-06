

from machine import Timer
import wb


tim_hub = Timer(1)

tim_hub.init(period=30, mode=Timer.PERIODIC, callback=wb.distribute)

wb.init()

wb.led.blue()

del Timer
del wb
