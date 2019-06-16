# frameHub.py

from wb import _TYPE_INIT, _TYPE_RESPONSE, _TYPE_REPORT, _TYPE_INSERT
from ModuleManager import moduleManager as mMag
from machine import reset, Pin
import wb

# from machine import UART
# uart2 = UART(1, 125000)
# uart2.init(125000, bits=8, parity=None, stop=1, tx=10, rx=9)

# def print_s(buf):
#     for data in buf:
#         print(data, end=',')
#     print(' ')

flag = False
button = Pin(26, Pin.IN, value=1, pull=Pin.PULL_UP)

def distribute(t):
    # wb.send_a_data(0)
    wb.hub.handle()
    # if flag == False:
    #     wb.send_a_data(0xF0)
    #     wb.send_a_data(wb.hub.available())
    if button.value() == 0:
        reset()
    while wb.hub.available():
        # _handle(_buf.pop(0))
        buf = wb.hub.get_msg()
        # print(buf)
        # print_s(buf)
        if button.value() == 0:
            reset()
        if buf[2] == _TYPE_INIT:
            wb.module_manager.put(buf)
        elif buf[2] == _TYPE_RESPONSE:
            wb.hub.set_response(buf[1], buf)
        elif buf[2] == _TYPE_REPORT:
            mMag.doReport(buf[1], buf)
        elif buf[2] == _TYPE_INSERT and flag == True:
            reset()
        # else:
        #     print_s(buf[:(4 + buf[3])])

        # uart2.write('end')
    # wb.send_a_data(0xFF)


def getResponse(self, addr):
    # if addr in _responseCache:
    #     return _responseCache[addr]
    # else:
    #     return None
    pass
