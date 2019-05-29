# Receiver.py
from syspublic import MSG_START_TAG, MSG_END_TAG, MSG_TRANSLATE_TAG, MSG_MAX_LENGTH_ALL
from public import _Addr_Master, _Addr_Broadcast, _Addr_Init
from Tool import crc
from array import array

_rec_buf = array('B', [0, 0, 0, 0])


def print_s(buf):
    for data in buf:
        print(data, end=',')
    print(' ')


def translate_check(buf):
    # hbase = 5
    # print('translate_check')
    # print('0:', buf[0])
    if MSG_START_TAG != buf[0]:
        return False
    # print('1:', buf[1])
    if (_Addr_Master != buf[1]) and (_Addr_Broadcast != buf[1]):
        return False
    # print('4:', buf[4])
    if buf[4] > (MSG_MAX_LENGTH_ALL - 7):
        return False
    # print('2:', buf[2])
    if (buf[2] < 0x10) and (_Addr_Init != buf[2]):
        return False
    i = buf[4]
    j = 0
    chr_check = _rec_buf
    while (MSG_END_TAG != buf[i]) and (i < MSG_MAX_LENGTH_ALL):
        data_buffer = buf[5 + i]
        i = i + 1
        if data_buffer == MSG_TRANSLATE_TAG:
            data_buffer = buf[5 + i]
            i = i + 1
        chr_check[j] = data_buffer
        j = j + 1
        if (j >= 4):
            break

    # buf[buf[4] + 5] = chr_check[0]
    # buf[buf[4] + 6] = chr_check[1]

    state = False
    crc_buf = (crc.create_of_len(buf, buf[4] + 5))
    if (crc_buf[0] == chr_check[0]) and (crc_buf[1] == chr_check[1]):
        state = True
    # print_s(buf)
    i = 1
    j = 0
    buf_len = buf[4] + 5
    while (i < buf_len) and (i < MSG_MAX_LENGTH_ALL):
        data_buffer = buf[i]
        i = i + 1
        if data_buffer == MSG_TRANSLATE_TAG:
            data_buffer = buf[i]
            i = i + 1
        buf[j] = data_buffer
        j = j + 1
    buf[3] = j - 4
    # print_s(buf)
    return state
