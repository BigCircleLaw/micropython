# Tool.py
from array import array
from micropython import const

_POLYNOMIAL = const(0x1021)
_INITIAL_REMAINDER = const(0x0000)
_WIDTH = const(16)
_SHIFT = const(_WIDTH - 8)
_TOPBIT = const(1 << (_WIDTH - 1))


class CRC:

    _crcTable = array('H')

    def __init__(self):
        for step in range(0, 256):
            remainder = step << _SHIFT
            for bit in range(8, 0, -1):
                if remainder & _TOPBIT:
                    remainder = ((remainder << 1) & 0xFFFF) ^ _POLYNOMIAL
                else:
                    remainder = remainder << 1
            CRC._crcTable.append(remainder)

    def create(self, buf):
        remainder = _INITIAL_REMAINDER
        for byte in buf:
            remainder = CRC._crcTable[byte ^ (remainder >> (_SHIFT))] ^ (
                (remainder << 8) & 0xFFFF)
        crc = [(remainder & 0xff00) >> 8, remainder & 0x00ff]
        return crc

    def create_of_len(self, buf, buf_len):
        remainder = _INITIAL_REMAINDER
        for position in range(buf_len):
            remainder = CRC._crcTable[buf[position] ^ (
                remainder >> (_SHIFT))] ^ ((remainder << 8) & 0xFFFF)
        crc = [(remainder & 0xff00) >> 8, remainder & 0x00ff]
        return crc


crc = CRC()
