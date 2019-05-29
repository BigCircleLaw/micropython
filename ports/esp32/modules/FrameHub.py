# frameHub.py
from syspublic import Head, MSG_MAX_LENGTH_ALL, MSG_START_TAG, MSG_END_TAG, MSG_TRANSLATE_TAG
from public import _TYPE_INIT, _TYPE_RESPONSE, _TYPE_REPORT, _TYPE_INSERT
from ModuleManager import moduleManager as mMag
from micropython import const
from array import array
from Receiver import translate_check
from machine import reset, Pin

# from machine import UART
# uart2 = UART(1, 125000)
# uart2.init(125000, bits=8, parity=None, stop=1, tx=10, rx=9)

_HUB_MAX = const(50)
_HUB_RESPONSE_MAX = const(3)


def print_s(buf):
    for data in buf:
        print(data, end=',')
    print(' ')


class Hub:
    flag = False

    def __init__(self):
        self._buf = array('B',
                          [0 for i in range(_HUB_MAX * MSG_MAX_LENGTH_ALL)])
        self._buf_p = memoryview(self._buf)
        self._head = 0
        self._num = 0
        self._tail = 0
        self._index = 0
        self._responseCache = {}
        self.flag = False
        self.button = Pin(26, Pin.IN, value=1, pull=Pin.PULL_UP)

    def put(self, dataList):
        if self._num >= _HUB_MAX:
            return
        start_position = 0
        end_position = 0
        for data in dataList:
            if data == MSG_START_TAG:
                start_position = self._head * MSG_MAX_LENGTH_ALL
                end_position = (self._head + 1) * MSG_MAX_LENGTH_ALL
                self._index = start_position
                # print('shishi = ', end = '')
            self._buf[self._index] = data
            self._index = self._index + 1
            if self._index >= end_position:
                self._index = end_position - 1

            if data == MSG_END_TAG and ((self._index - start_position) > 6):
                # print(self._head)
                # print_s(self._buf_p[start_position:end_position])
                if translate_check(self._buf_p[start_position:end_position]):
                    # print_s(self._buf_p[start_position:end_position])
                    # Remove the  start character of  the  packet
                    self._num = self._num + 1
                    self._head = (self._head + 1) % _HUB_MAX

    def distribute(self, t):
        # uart2.write('start')
        # uart2.write(str(len(self._buf)))
        if self.button.value() == 0:
            reset()
        while not self._num == 0:
            # self._handle(self._buf.pop(0))
            if self.button.value() == 0:
                reset()
            start_position = self._tail * MSG_MAX_LENGTH_ALL
            end_position = (self._tail + 1) * MSG_MAX_LENGTH_ALL
            buf = self._buf_p[start_position:end_position]
            # print(start_position, end_position)
            # print_s(buf[:(4 + buf[3])])
            if buf[2] == _TYPE_INIT:
                mMag.put(buf[4:(4 + buf[3])])
            elif buf[2] == _TYPE_RESPONSE:
                self._responseCache[buf[1]] = buf
            elif buf[2] == _TYPE_REPORT:
                mMag.doReport(buf[1], buf)
            elif buf[2] == _TYPE_INSERT and self.flag == True:
                reset()
            # else:
            #     print_s(buf[:(4 + buf[3])])

            self._tail = (self._tail + 1) % _HUB_MAX
            self._num = self._num - 1
        # uart2.write('end')

    def getbuf(self):
        return self._buf

    def getResponse(self, addr):
        if addr in self._responseCache:
            return self._responseCache[addr]
        else:
            return None


hub = Hub()
