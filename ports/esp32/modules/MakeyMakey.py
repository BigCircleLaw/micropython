# MakeyMakey.py
"""
创意键盘模块/MakeyMakey
=============================
共有18个通道分为三组，一组触摸，一组鼠标和一组键盘

通过USB连接在电脑时：
触摸组拥有键盘上下左右，空格和鼠标左键的效果；
鼠标组可以实现鼠标的上下左右移动以及左键右键点击效果；
键盘组拥有键盘WASDFG的按键效果。

"""

from public import DEVICE_TYPE, _TYPE_REQUEST, RGB_Y, RGB_B
from ModuleObj import ModuleObj, constrain
from syspublic import Msg
from dataFormat import _DataFormat
import time
from EventManager import EventNameList, _return_event_start, _set_event_value, EventManager

_CMD_HALL_Calibration = 0x08


class MakeyMakey(ModuleObj):
    class _Event(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, MakeyMakey, id, nameList)

    class _Register(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, MakeyMakey, id, nameList)

        def touch(self, interval=50):
            """
                注册触摸组值上传，当触摸组的任意通道发生触摸或触摸放手时会接收到数据，返回类型为list(bool)

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(0, EventManager._LIST_VALUE_TYPE,
                                           self.get_name('touch'))
            return register._register(EventManager._CHANGED_ACTION, None,
                                      interval)

        def mouse(self, interval=50):
            """
                注册鼠标组值上传，当鼠标组的任意通道发生触摸或触摸放手时会接收到数据，返回类型为list(bool)

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(1, EventManager._LIST_VALUE_TYPE,
                                           self.get_name('mouse'))
            return register._register(EventManager._CHANGED_ACTION, None,
                                      interval)

        def keyboard(self, interval=50):
            """
                注册键盘组值上传，当键盘组的任意通道发生触摸或触摸放手时会接收到数据，返回类型为list(bool)

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(2, EventManager._LIST_VALUE_TYPE,
                                           self.get_name('keyboard'))
            return register._register(EventManager._CHANGED_ACTION, None,
                                      interval)

    class _UnRegister(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, MakeyMakey, id, nameList)

        def touch(self, interval=50):
            """
                注销触摸组值上传

                """
            unregister = _return_event_start(0, EventManager._LIST_VALUE_TYPE,
                                             self.get_name('touch'))
            return unregister._unregister()

        def mouse(self, interval=50):
            """
                注销鼠标组值上传

                """
            unregister = _return_event_start(1, EventManager._LIST_VALUE_TYPE,
                                             self.get_name('mouse'))
            return unregister._unregister()

        def keyboard(self, interval=50):
            """
                注销键盘组值上传

                """
            unregister = _return_event_start(2, EventManager._LIST_VALUE_TYPE,
                                             self.get_name('keyboard'))
            return unregister._unregister()

    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['makeyMakey'])
        self._data_own = [[False for j in range(6)] for i in range(3)]
        self._data_value = [0, 0, 0]

        self._name_list = list()
        self.event = MakeyMakey._Event(id, self._name_list)
        self.register = MakeyMakey._Register(id, self._name_list)
        self.unregister = MakeyMakey._UnRegister(id, self._name_list)

    def _get_data(self, frame):
        
        
        temp = _DataFormat(['B', 'B', 'B'])
        self._data_value = temp.get_data_list(frame[4:])

        for i in range(6):
            self._data_own[0][i] = (self._data_value[0] & 0x01 << i) != 0
            self._data_own[1][i] = (self._data_value[1] & 0x01 << i) != 0
            self._data_own[2][i] = (self._data_value[2] & 0x01 << i) != 0

        _set_event_value(self._name_list, self._data_own)

    def is_touching(self, channel):
        """
            获取触摸组的某通道是否被触摸

            Parameters
            ----------
            channel : int
                通道号：1~6
            
            Returns
            -------
            bool
                True: 该通道被触摸
                False: 该通道没有被触摸

            Metas
            ---------------
            in :channel
                range: 1~6
                
            Examples
            -------

            .. code-block:: python

                # 实时显示触摸组1,2,6通道是否被触摸
                from wonderbits import MakeyMakey, Display
                makeyMakey1 = MakeyMakey()
                display1 = Display()

                while True:
                    display1.print(1, 1, makeyMakey1.is_touching(1))
                    display1.print(1, 9, makeyMakey1.is_touching(2))
                    display1.print(2, 1, makeyMakey1.is_touching(6))
                
            """
        channel = constrain(channel, 1, 6) - 1
        return self._data_own[0][channel]

    def is_mouse_connected(self, channel):
        """
            获取鼠标组的某通道是否被导通

            Parameters
            ----------
            channel : int
                通道号：1~6
            
            Returns
            -------
            bool
                True: 该通道被导通
                False: 该通道没有被导通

            Metas
            ---------------
            in :channel
                range: 1~6
                
            Examples
            -------

            .. code-block:: python

                # 实时显示鼠标组1,2,6通道是否被导通
                from wonderbits import MakeyMakey, Display
                makeyMakey1 = MakeyMakey()
                display1 = Display()

                while True:
                    display1.print(1, 1, makeyMakey1.is_mouse_connected(1))
                    display1.print(1, 9, makeyMakey1.is_mouse_connected(2))
                    display1.print(2, 1, makeyMakey1.is_mouse_connected(6))
                
            """
        channel = constrain(channel, 1, 6) - 1
        return self._data_own[1][channel]

    def is_keyboard_connected(self, channel):
        """
            获取键盘组的某通道是否被导通

            Parameters
            ----------
            channel : int
                通道号：1~6
            
            Returns
            -------
            bool
                True: 该通道被导通
                False: 该通道没有被导通

            Metas
            ---------------
            in :channel
                range: 1~6
                
            Examples
            -------

            .. code-block:: python

                # 实时显示键盘组1,2,6通道是否被导通
                from wonderbits import MakeyMakey, Display
                makeyMakey1 = MakeyMakey()
                display1 = Display()

                while True:
                    display1.print(1, 1, makeyMakey1.is_keyboard_connected(1))
                    display1.print(1, 9, makeyMakey1.is_keyboard_connected(2))
                    display1.print(2, 1, makeyMakey1.is_keyboard_connected(6))
                
            """
        channel = constrain(channel, 1, 6) - 1
        return self._data_own[2][channel]
