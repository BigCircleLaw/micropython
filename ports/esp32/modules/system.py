# system.py
from syspublic import led
from machine import Timer
from Uart import uart
from FrameHub import hub
from ModuleManager import moduleManager as mMag
import time
from public import DEVICE_TYPE
import gc

# import _thread

# def uart_handle():
#     while True:
#         uart.RxProcess(1)
#         time.sleep_ms(30)

# def hub_handle():
#     while True:
#         hub.distribute(1)
#         time.sleep_ms(40)

# _thread.stack_size(10240)
# _thread.start_new_thread(uart_handle, ())
# _thread.stack_size(10240)
# _thread.start_new_thread(hub_handle, ())

print(time.ticks_ms())
led.Red()

tim_serial = Timer(2)
tim_hub = Timer(1)
tim_serial.init(period=20, mode=Timer.PERIODIC, callback=uart.RxProcess)
tim_hub.init(period=50, mode=Timer.PERIODIC, callback=hub.distribute)

mMag.start()

print(time.ticks_ms())
# mMag.setID()
_m_info = mMag.getTypeAddrBuf()
_module_key_list = list(DEVICE_TYPE.keys())
_module_value_list = list(DEVICE_TYPE.values())
_m_value_position = 1
_module_info = []
mf = open('sysCfg.py', 'wb')
for i in range(_m_info[0]):
    if _m_info[_m_value_position] in _module_value_list:
        mStr = _module_key_list[_module_value_list.index(
            _m_info[_m_value_position])]
        mStr2 = mStr[0].upper() + mStr[1:]
        _m_value_position = _m_value_position + 1
        mf.write(bytearray('from ' + mStr2 + ' import ' + mStr2 + '\r\n'))
        for j in range(_m_info[_m_value_position]):
            mf.write(
                bytearray(mStr + str(j + 1) + '=' + mStr2 + '(' + str(j + 1) +
                          ')\r\n'))
            # print(mStr + str(j + 1) + '=' + mStr + '(' + str(j + 1) + ')')
            _module_info.append(mStr + str(j + 1))
        _m_value_position = _m_value_position + 1
        # print(mStr)
        del mStr
        del j
    else:
        _m_value_position = _m_value_position + 2
# del i

mf.close()
del _m_info
del _module_key_list
del _module_value_list
del _m_value_position
del mf
gc.collect()

print(time.ticks_ms())
time.sleep_ms(10)
hub.flag = True
time.sleep_ms(10)
# mMag.doUpdate()
led.Blue()


def getModuleInformation():
    return _module_info
