import struct
from array import array
from syspublic import MSG_MAX_LENGTH_ALL

# from machine import UART
# uart2 = UART(1, 125000)
# uart2.init(125000, bits=8, parity=None, stop=1, tx=10, rx=9)

# [b, B, h, H, i, I, l, L, q, Q, f, d]


def print_s(buf):
    for data in buf:
        print(data, end=',')
    print(' ')


class _DataFormat():
    # _finalData = []
    _data_name = ['b', 'B', 'h', 'H', 'l', 'L', 'f']
    _send_buf = array('B', [0 for i in range(MSG_MAX_LENGTH_ALL)])
    _send_buf_p = memoryview(_send_buf)

    def __init__(self, format):
        self._defFormat = format.copy()

    def get_list(self, data):
        temp = self._send_buf_p
        count = 4
        for i in range(len(self._defFormat)):
            if isinstance(data[i], list):
                # p = self._toList(value)
                for j in data[i]:
                    temp[count] = j
                    count = count + 1
            elif isinstance(data[i], str):
                for p in data[i]:
                    temp[count] = ord(p)
                    count = count + 1
            else:
                if self._defFormat[i] != 'f':
                    data[i] = int(data[i])
                for p in struct.pack('<' + self._defFormat[i], data[i]):
                    temp[count] = p
                    count = count + 1
        # print_s(temp[:count])
        return temp[:count]

        # self._finalData = self._toList(self._int_to_list(data))
        # return self._finalData

    def get_data_list(self, data):
        s = ''
        for i in self._defFormat:
            if i in _DataFormat._data_name:
                s += i
            else:
                break
        return list(struct.unpack('<' + s, bytes(data)))
