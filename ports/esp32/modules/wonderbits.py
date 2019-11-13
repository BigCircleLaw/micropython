import wb
from ModuleManager import moduleManager as mMag
from system import _module_info
from public import DEVICE_TYPE
import os

VERSION = (0, 2, 5)
__version__ = '.'.join(map(str, VERSION))

state = 'main.py' not in os.listdir()

_m_info = wb.module_manager.get_type_num_buf()
# print(_m_info)
if _m_info[0] > 0:
    _module_key_list = list(DEVICE_TYPE.keys())
    _module_value_list = list(DEVICE_TYPE.values())
    _m_value_position = 1

    for i in range(_m_info[0]):
        if _m_info[_m_value_position] in _module_value_list:
            mStr = _module_key_list[_module_value_list.index(
                _m_info[_m_value_position])]
            mStr2 = mStr[0].upper() + mStr[1:]
            _m_value_position = _m_value_position + 1
            exec('from ' + mStr2 + ' import ' + mStr2)
            # print('from ' + mStr2 + ' import ' + mStr2)
            # if state:
            for j in range(_m_info[_m_value_position]):
                exec(mStr + str(j + 1) + '=' + mStr2 + '(' + str(j + 1) + ')')
                # print(mStr + str(j + 1) + '=' + mStr2 + '(' + str(j + 1) + ')')
                _module_info.append(mStr + str(j + 1))

            _m_value_position = _m_value_position + 1
        else:
            print('not support module :', _m_info[_m_value_position], '!')
            _m_value_position = _m_value_position + 2

    del _module_key_list
    del _module_value_list
    del _m_value_position
    del state
    del i
    del mStr
    del mStr2
    del j

del wb
del mMag
del DEVICE_TYPE

del _m_info


class wb_tool(object):
    """
    豌豆拼工具集合
    """

    @staticmethod
    def show_console():
        pass

    @staticmethod
    def hide_console():
        pass


from Event import Event
