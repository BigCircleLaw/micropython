# ModuleObj.py
# from syspublic import  *
from public import _Addr_Error, _TYPE_REQUEST, _CMD_LED, _CMD_GET_VERSION
from FrameHub import hub
from ModuleManager import moduleManager as mMag
import time
from dataFormat import _DataFormat


class ModuleObj:
    def __init__(self, Id, Type):
        self.Id = Id
        self.Type = Type
        # self.dstAddr = _Addr_Error
        self.dstAddr = mMag.getAddr(self.Id, self.Type)
        mMag.defineNewModule(self)

    def setAddr(self):
        self.dstAddr = mMag.getAddr(self.Id, self.Type)

    def _send_with_ack(self, type, data, timeout):
        if self.dstAddr == _Addr_Error:
            return None
        mMag.sendACK(self.dstAddr, type, data)
        time.sleep_us(500)
        while timeout:
            response = hub.getResponse(self.dstAddr)
            if response != None:
                return response
            time.sleep_us(1000)
            timeout = timeout - 1
        return None

    def _send_without_ack(self, type, data):
        if self.dstAddr == _Addr_Error:
            return
        mMag.sendACK(self.dstAddr, type, data)
        time.sleep_us(500)

    def set_onboard_rgb(self, rgb):
        """
            设置板载LED的颜色

            Parameters
            ----------
            rgb : int=RGB_R:1,RGB_G:2,RGB_B:3,RGB_LB:4,RGB_Y:5,RGB_P:6,RGB_W:7,RGB_OFF:8
                颜色：只支持8种颜色
            Returns
            -------
            
            """
        data = _DataFormat(['B', 'B'])
        self._send_without_ack(_TYPE_REQUEST, data.get_list([_CMD_LED, rgb]))

    def get_firmware_version(self, CMD=0):
        data = _DataFormat(['B', 'B'])
        data = self._send_with_ack(_TYPE_REQUEST,
                                   data.get_list([_CMD_GET_VERSION, CMD]),
                                   500)[5:]
        if data == None:
            print('get_firmware_version fail!!!')
            return None
        return data[0] * 100 + data[1] * 10 + data[2]

    def _do_update_value(self):
        pass

    def _get_data(self):
        pass


def constrain(amt, low, high):
    return low if amt < low else (high if amt > high else amt)


def _value_comparison(newValue, oldValue, varyValue):
    return abs(newValue - oldValue) >= varyValue, oldValue if abs(
        newValue - oldValue) < varyValue else newValue
