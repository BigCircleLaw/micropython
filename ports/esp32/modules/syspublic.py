# syspublic.py
from machine import Pin
from micropython import const

MSG_MAX_LENGTH_ALL = const(45)

MSG_START_TAG = const(0xFF)
MSG_END_TAG = const(0xFE)
MSG_TRANSLATE_TAG = const(0xFD)


class LED:
    _LED_ON = 0
    _LED_OFF = 1
    LED_Red = Pin(32, Pin.OUT, value=1)
    LED_Green = Pin(33, Pin.OUT, value=1)
    LED_Blue = Pin(27, Pin.OUT, value=1)

    def __init__(self):
        pass

    def Red(self):
        self.LED_Red.value(self._LED_ON)
        self.LED_Green.value(self._LED_OFF)
        self.LED_Blue.value(self._LED_OFF)

    def Green(self):
        self.LED_Red.value(self._LED_OFF)
        self.LED_Green.value(self._LED_ON)
        self.LED_Blue.value(self._LED_OFF)

    def Blue(self):
        self.LED_Red.value(self._LED_OFF)
        self.LED_Green.value(self._LED_OFF)
        self.LED_Blue.value(self._LED_ON)

    def Yellow(self):
        self.LED_Red.value(self._LED_ON)
        self.LED_Green.value(self._LED_ON)
        self.LED_Blue.value(self._LED_OFF)

    def Lblue(self):
        self.LED_Red.value(self._LED_OFF)
        self.LED_Green.value(self._LED_ON)
        self.LED_Blue.value(self._LED_ON)

    def Purple(self):
        self.LED_Red.value(self._LED_ON)
        self.LED_Green.value(self._LED_OFF)
        self.LED_Blue.value(self._LED_ON)

    def White(self):
        self.LED_Red.value(self._LED_ON)
        self.LED_Green.value(self._LED_ON)
        self.LED_Blue.value(self._LED_ON)

    def black(self):
        self.LED_Red.value(self._LED_OFF)
        self.LED_Green.value(self._LED_OFF)
        self.LED_Blue.value(self._LED_OFF)


led = LED()


class Head:
    def __init__(self):
        pass

    def getFrameHead(self, frame):
        self._frame = frame
        self.targetAdd = self._frame[0]
        self.sourceAdd = self._frame[1]
        self.type = self._frame[2]
        self.datalength = self._frame[3]
        self.framelength = self.datalength + self.size()

    # def setLength(self, length):
    #     if self._frame:
    #         self._frame[3] = self.datalength

    def size(self):
        return 4


class Msg:

    head = Head()
    data = []

    def __init__(self, targetAdd=0, sourceAdd=0, type=0, length=0, data=[]):
        pass
        # self.head.targetAdd = targetAdd
        # self.head.sourceAdd = sourceAdd
        # self.head.type = type
        # self.head.length = length
        # self.data = data

    def getMsg(self, frame):
        pass
        # self.head.getFrameHead(frame)
        # self.data = frame[self.head.size():len(frame)]
