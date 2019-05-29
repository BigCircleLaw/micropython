# Uart.py
from machine import UART
from FrameHub import hub


class Uart:
    def __init__(self):
        # self.uart2 = UART(2, 125000)
        # self.uart2.init(125000, bits=8, parity=None,
        #                 stop=1, tx=17, rx=16)  # init uart
        self.uart2 = UART(1, 125000)
        self.uart2.init(125000, bits=8, parity=None, stop=1, tx=10, rx=9)

    def RxProcess(self, t):
        # while self.uart2.any() > 0:
        #     rec.put(self.uart2.read(1)[0])
        n = self.uart2.any()
        # self.uart2.write(str(n))
        if n > 0:
            hub.put(self.uart2.read(n))
        # print('n:', n)
        # self.uart2.write(bytearray(str(n)))
        # self.uart2.write('end')

    def send(self, data, length):
        self.uart2.write(data, length)


uart = Uart()
