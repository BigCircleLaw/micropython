# Hall.py
"""
霍尔模块/Hall
=============================
内置霍尔传感器，可以测量磁场强度。

"""

from public import DEVICE_TYPE, _TYPE_REQUEST, RGB_Y, RGB_B
from ModuleObj import ModuleObj, constrain
from syspublic import Msg
from dataFormat import _DataFormat
import time
from EventManager import EventNameList, _return_event_start, _set_event_value, EventManager

_CMD_HALL_Calibration = 0x08


class Hall(ModuleObj):
    class _Event(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Hall, id, nameList)

        def magnetic_changed(self, delta=1, interval=50):
            """
                当霍尔检测的磁场强度值发生改变时会执行事件修饰的函数

                Parameters
                ----------
                delta : int
                    用于设置触发要求：值改变超过delta才符合触发条件
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :delta
                    default: 1
                    range: 1~10
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(0, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('magnetic'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

    class _Register(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Hall, id, nameList)

        def magnetic(self, delta=1, interval=50):
            """
                注册霍尔检测的磁场强度值上传，当霍尔检测的磁场强度值改变会接收到数据，返回类型为float

                Parameters
                ----------
                delta : int
                    用于设置触发要求：值改变超过delta才符合触发条件
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求，如果符合会发送对应内容

                Metas
                ---------------
                in :delta
                    default: 1
                    range: 1~10
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(
                0,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('magnetic'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

    class _UnRegister(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Hall, id, nameList)

        def magnetic(self):
            """
                注销霍尔检测的磁场强度值上传

                """
            unregister = _return_event_start(
                0,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('magnetic'),
            )
            unregister._unregister()

    _HallDelayContValue_ = 0

    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['hall'])
        self._data_own = [0]

        self._name_list = list()
        self.event = Hall._Event(id, self._name_list)
        self.register = Hall._Register(id, self._name_list)
        self.unregister = Hall._UnRegister(id, self._name_list)

    def _get_data(self, frame):
        
        
        temp = _DataFormat(['h'])
        self._data_own[0] = round(temp.get_data_list(frame[4:])[0] / 5.05, 2)

        _set_event_value(self._name_list, self._data_own)

    def get_magnetic(self):
        """
            获取磁场强度值

            Parameters
            ----------

            Returns
            -------
            float
                磁场强度值（符号表示方向，绝对值表示强度），范围 -100~100

            Metas
            ---------------
            out :
                range: -100~100
                
            Examples
            -------

            .. code-block:: python

                # 实时检测磁场强度
                from wonderbits import Hall, Display
                hall1 = Hall()
                display1 = Display()

                while True:
                    display1.print(1, 1, hall1.get_magnetic())
                

            """
        return self._data_own[0]

    def calibrate(self, block=True):
        """
            校准霍尔传感器
            **注意**：校准过程中请确保没有磁性物体靠近模块，否则会导致校准后不准确。
            校准时，模块指示灯会变为黄色，等待指示灯变蓝说明校准完成了。

            Parameters
            ----------
            block : bool
                阻塞参数
                False: 不阻塞
                True: 阻塞

            Metas
            ---------------
            in :block
                default: True
                
            Examples
            -------

            .. code-block:: python

                # 校准霍尔传感器，并实时检测磁场强度
                from wonderbits import Hall, Display
                hall1 = Hall()
                display1 = Display()

                display1.print(1,1,'calibrating..')
                hall1.calibrate()  # 校准传感器，程序将阻塞在这儿一段时间
                display1.print(1,1,'calibrated.  ')

                while True:
                    display1.print(1, 1, hall1.get_magnetic())
            """
        self.set_onboard_rgb(RGB_Y)
        if Hall._HallDelayContValue_ == 0:
            if block:
                time.sleep_ms(1300)
            Hall._HallDelayContValue_ = 1
        temp = _DataFormat(['B'])
        if block:
            self._send_with_ack(_TYPE_REQUEST,
                                temp.get_list([_CMD_HALL_Calibration]), 500)
        else:
            self._send_without_ack(_TYPE_REQUEST,
                                   temp.get_list([_CMD_HALL_Calibration]))
        self.set_onboard_rgb(RGB_B)
