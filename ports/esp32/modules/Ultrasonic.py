# Ultrasonic.py
"""
超声波测距模块/Ultrasonic
=============================
此模块可以测量物体距该模块的距离。
它利用声波遇到障碍物会反弹的原理，测量发射声波和收到反弹声波的时间差可以计算出与障碍物之间的距离。
"""

from public import DEVICE_TYPE, _TYPE_REQUEST
from ModuleObj import ModuleObj, constrain
from syspublic import Msg
from dataFormat import _DataFormat
from EventManager import EventNameList, _return_event_start, _set_event_value, EventManager

# from machine import UART
# uart2 = UART(1, 125000)
# uart2.init(125000, bits=8, parity=None, stop=1, tx=10, rx=9)


class Ultrasonic(ModuleObj):
    class _Event(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Ultrasonic, id, nameList)

        def distance_changed(self, delta=10, interval=50):
            """
                当超声波检测的距离值发生改变时会执行事件修饰的函数

                Parameters
                ----------
                delta : int
                    用于设置触发要求：值改变超过delta才符合触发条件
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :delta
                    default: 100
                    range: 10~1000
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(0, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('distance'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

    class _Register(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Ultrasonic, id, nameList)

        def distance(self, delta=10, interval=50):
            """
                注册超声波检测的距离值上传，当超声波检测的距离值改变会接收到数据，返回类型为float

                Parameters
                ----------
                delta : int
                    用于设置触发要求：值改变超过delta才符合触发条件
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求，如果符合会发送对应内容

                Metas
                ---------------
                in :delta
                    default: 100
                    range: 10~1000
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(
                0,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('distance'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

    class _UnRegister(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Ultrasonic, id, nameList)

        def distance(self):
            """
                注销超声波检测的距离值上传

                """
            unregister = _return_event_start(0,
                                             EventManager._NUMBER_VALUE_TYPE,
                                             self.get_name('distance'))
            unregister._unregister()

    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['ultrasonic'])
        self._data_own = [0]
        self._name_list = list()
        self.event = Ultrasonic._Event(id, self._name_list)
        self.register = Ultrasonic._Register(id, self._name_list)
        self.unregister = Ultrasonic._UnRegister(id, self._name_list)

    def _get_data(self, frame):
        temp = _DataFormat(['h'])
        valueLocal = temp.get_data_list(frame[4:])
        if valueLocal[0] > 19:
            self._data_own[0] = valueLocal[0] / 10

        _set_event_value(self._name_list, self._data_own)

    def get_distance(self):
        """
            获取超声波检测的距离值（cm）

            Parameters
            ----------

            Returns
            -------
            float
                距离值，范围 0~400 cm

            Metas
            ---------------
            out :
                range: 0~400
                
            Examples
            -------

            .. code-block:: python

                # 显示超声波检测的距离值
                from wonderbits import Ultrasonic, Display
                ultrasonic1 = Ultrasonic()
                
                while True:
                    display1.print(1, 1, ultrasonic1.get_distance())

            """
        return self._data_own[0]
