# ModuleObj.py
# from syspublic import  *
from wb import _Addr_Error, _TYPE_REQUEST, _CMD_LED, _CMD_GET_VERSION

from ModuleManager import moduleManager as mMag
import time
from wb import _DataFormat, module_manager, hub


class ModuleObj(object):
    def __new__(cls, Id=1):
        Id = Id - 1
        state, module = mMag.findModuleList(Id, cls._type)
        if state:
            module.state = False
        else:
            module = object.__new__(cls)
            module.state = True
        return module

    def __init__(self, Id):

        if self.state:
            self.id = Id
            # self.dstAddr = _Addr_Error
            self.dstAddr = module_manager.get_addr(self.id, self._type)
            self.state = True
            mMag.defineNewModule(self)

    def _send_with_ack(self, type, data, timeout):
        if self.dstAddr == _Addr_Error:
            return None
        module_manager.send_ack(self.dstAddr, type, data)
        # time.sleep_us(500)
        while timeout:
            response = hub.get_response(self.dstAddr)
            if response != None:
                return response
            time.sleep_us(1000)
            timeout = timeout - 1
        return None

    def _send_without_ack(self, type, data):
        if self.dstAddr == _Addr_Error:
            return
        module_manager.send_ack(self.dstAddr, type, data)
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
        data = _DataFormat('BB')
        self._send_without_ack(_TYPE_REQUEST, data.get_list([_CMD_LED, rgb]))

    def get_firmware_version(self, CMD=0):
        data = _DataFormat('BB')
        data = self._send_with_ack(_TYPE_REQUEST,
                                   data.get_list([_CMD_GET_VERSION, CMD]), 500)
        if data == None:
            print('get_firmware_version fail!!!')
            return None
        # return data
        return data[4] * 100 + data[5] * 10 + data[6]

    def _do_update_value(self):
        pass

    def _get_data(self):
        pass


# def constrain(amt, low, high):
#     return low if amt < low else (high if amt > high else amt)

# def _value_comparison(newValue, oldValue, varyValue):
#     return abs(newValue - oldValue) >= varyValue, oldValue if abs(
#         newValue - oldValue) < varyValue else newValue
