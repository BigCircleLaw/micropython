# Pulse.py
"""
脉搏模块/Pulse
=============================
此模块可以测量人的脉搏，也可以获取脉搏波形用于显示

"""

from public import DEVICE_TYPE, _TYPE_REQUEST
from ModuleObj import ModuleObj, constrain
from syspublic import Msg
from dataFormat import _DataFormat
from EventManager import EventNameList, _return_event_start, _set_event_value, EventManager


class Pulse(ModuleObj):
    class _Event(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Pulse, id, nameList)

        def heart_rate_changed(self, delta=5, interval=200):
            """
                当模块检测的脉搏发生改变时会执行事件修饰的函数

                Parameters
                ----------
                delta : int
                    用于设置触发要求：值改变超过delta才符合触发条件
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :delta
                    default: 5
                    range: 5~20
                in :interval
                    default: 200
                    range: 200~60000

                """
            event = _return_event_start(1, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('heart_rate'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def heart_wave_received(self, interval=30):
            """
                当模块更新脉搏波形值时会执行事件修饰的函数

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 30
                    range: 30~60000

                """
            event = _return_event_start(0, EventManager._LIST_VALUE_TYPE,
                                        self.get_name('heart_wave_received'))
            return event._compare(EventManager._UPDATE_ACTION, None, interval)

    class _Register(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Pulse, id, nameList)

        def heart_rate(self, delta=5, interval=200):
            """
                注册模块检测的脉搏值上传，当模块检测的脉搏改变会接收到数据，返回类型为int

                Parameters
                ----------
                delta : int
                    用于设置触发要求：值改变超过delta才符合触发条件
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :delta
                    default: 5
                    range: 5~20
                in :interval
                    default: 200
                    range: 200~60000

                """
            register = _return_event_start(
                1,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('heart_rate'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def heart_wave_received(self, interval=30):
            """
                注册模块脉搏波形值上传，当模块更新脉搏波形值时会接收到数据，返回类型为list

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 30
                    range: 30~60000
                """
            register = _return_event_start(
                0, EventManager._LIST_VALUE_TYPE,
                self.get_name('heart_wave_received'))
            return register._register(EventManager._UPDATE_ACTION, None,
                                      interval)

    class _UnRegister(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Pulse, id, nameList)

        def heart_rate(self):
            """
                注销模块检测的脉搏值上传

                """
            unregister = _return_event_start(
                1,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('heart_rate'),
            )
            unregister._unregister()

        def heart_wave_received(self, delta=1, interval=50):
            """
                注销模块脉搏波形值上传

                """
            unregister = _return_event_start(
                0, EventManager._LIST_VALUE_TYPE,
                self.get_name('heart_wave_received'))
            return unregister._unregister()

    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['pulse'])
        self._data_own = [[], 0]
        self._dataOld = 0

        self._name_list = list()
        self.event = Pulse._Event(id, self._name_list)
        self.register = Pulse._Register(id, self._name_list)
        self.unregister = Pulse._UnRegister(id, self._name_list)

    def _get_data(self, frame):
        
        
        temp = _DataFormat(['B' for i in range(frame[3])])
        valueLocal = temp.get_data_list(frame[4:])
        self._data_own[0] = [round(i / 2.55, 2) for i in valueLocal[0:10]]
        self._data_own[
            1] = self._data_own[1] if frame[3] != 11 else valueLocal[10]

        _set_event_value(self._name_list, self._data_own)

    def get_heart_rate(self):
        """
            获取脉搏（每分钟脉搏跳动次数）
            测量时，从正面（有字的那面）将手指轻轻的贴在绿灯上，等待10秒左右方可测得准确的脉搏值

            Parameters
            ----------

            Returns
            -------
            int
                脉搏，范围 40~140

            Metas
            ---------------
            out :
                range: 40~140
                
            Examples
            -------

            .. code-block:: python

                # 检测并显示脉搏
                from wonderbits import Display, Pulse
                display1 = Display()
                pulse1 = Pulse()

                while True:
                    display1.print(1, 1, pulse1.get_heart_rate())

            """
        return self._data_own[1]

    def get_unread_wave_count(self):
        """
            获取脉搏波形队列中未读内容的个数（最多存储10个未读内容）
            返回为0时，说明没有未读取的内容

            Returns
            -------
            int
                未读内容的个数，范围 0~10

            Metas
            ---------------
            out :
                range: 0~10
                
            Examples
            -------
            未提供。可参考 `get_heart_wave`_ 的使用案例

            
            """
        return len(self._data_own[0])

    def get_heart_wave(self):
        """
            获取脉搏波形强度值
            如果没有未读的数据,则返回上一次的值

            Returns
            -------
            int
                脉搏波形强度，范围 0~255
            Metas
            ---------------
            out :
                range: 0~255
                
            Examples
            -------
            .. code-block:: python

                # 绘制脉搏波形
                from wonderbits import Display, Display
                display1 = Display()
                observer1 = Observer()

                x = 0   
                while True:
                    if pulse1.get_unread_wave_count():
                        x = x + 1
                        y = pulse1.get_heart_wave()/8
                        display1.draw_chart(x, y)
                    
                    if x >= 120:
                        x = 0            
            
            """
        if len(self._data_own[0]) == 1:
            self._value_plot = self._data_own[0].pop(0)
            return self._value_plot
        elif len(self._data_own[0]) == 0:
            return self._value_plot
        else:
            return self._data_own[0].pop(0)
