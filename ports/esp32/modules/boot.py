

from machine import Timer
from wb import distribute
from wb import init


tim_hub = Timer(1)

tim_hub.init(period=30, mode=Timer.PERIODIC, callback=distribute)

init()
