# Sender.py
from syspublic import MSG_START_TAG, MSG_END_TAG, MSG_TRANSLATE_TAG
# from public import *
from array import array
from syspublic import MSG_MAX_LENGTH_ALL
from Tool import crc


class Sender:
    def __init__(self):
        self._buf = array('B', [0 for i in range(MSG_MAX_LENGTH_ALL)])
        self._index = 0
        pass

    def _appendToBuf(self, byte):
        index = self._index
        if byte >= 0xfd:
            self._buf[index] = MSG_TRANSLATE_TAG
            index = index + 1
            self._buf[index] = byte - MSG_TRANSLATE_TAG
            index = index + 1
        else:
            self._buf[index] = byte
            index = index + 1
        self._index = index

    def _load(self, msg):
        self._buf[0] = MSG_START_TAG
        self._index = 1
        for i in msg:
            self._appendToBuf(i)

        self._buf[4] = self._index - 5
        CRC = crc.create_of_len(self._buf, self._index)
        self._appendToBuf(CRC[0])  # TODO: Add CRC bytes
        self._appendToBuf(CRC[1])
        self._buf[self._index] = MSG_END_TAG

    def send(self, msg):
        from Uart import uart
        self._load(msg)
        # print(self._buf)
        uart.send(self._buf, self._index + 1)


sender = Sender()
