# Observer.py
"""
监测模块/Observer
=============================
此模块可以监测环境中的温/湿度 、亮度 和声音强度

"""

from public import DEVICE_TYPE, _TYPE_REQUEST
from ModuleObj import ModuleObj, constrain
from syspublic import Msg
from dataFormat import _DataFormat
from EventManager import EventNameList, _return_event_start, _set_event_value, EventManager


class Observer(ModuleObj):
    class _Event(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Observer, id, nameList)

        def temperature_changed(self, delta=1, interval=50):
            """
                当模块检测到的温度值发生改变时会执行事件修饰的函数

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
                    range: 1~5
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(3, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('temperature'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def humidity_changed(self, delta=1, interval=50):
            """
                当模块检测到的湿度值发生改变时会执行事件修饰的函数

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
            event = _return_event_start(2, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('humidity'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def light_changed(self, delta=5, interval=50):
            """
                当模块检测到的亮度值发生改变时会执行事件修饰的函数

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
                    range: 5~50
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(0, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('light'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def volume_changed(self, delta=5, interval=50):
            """
                当模块检测到的声音强度值发生改变时会执行事件修饰的函数

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
                    range: 5~50
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(1, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('volume'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

    class _Register(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Observer, id, nameList)

        def temperature(self, delta=1, interval=50):
            """
                注册模块检测的温度值上传，当模块检测的温度值改变会接收到数据，返回类型为int

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
                    range: 1~5
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(
                3,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('temperature'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def humidity(self, delta=1, interval=50):
            """
                注册模块检测的湿度值上传，当模块检测的湿度值改变会接收到数据，返回类型为int

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
                2,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('humidity'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def light(self, delta=5, interval=50):
            """
                注册模块检测的亮度值上传，当模块检测的亮度值改变会接收到数据，返回类型为int

                Parameters
                ----------
                delta : int
                    用于设置触发要求：值改变超过delta才符合触发条件
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求，如果符合会发送对应内容

                Metas
                ---------------
                in :delta
                    default: 5
                    range: 5~50
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(
                0,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('light'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def volume(self, delta=5, interval=50):
            """
                注册模块检测的声音强度值上传，当模块检测的声音强度值改变会接收到数据，返回类型为int

                Parameters
                ----------
                delta : int
                    用于设置触发要求：值改变超过delta才符合触发条件
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求，如果符合会发送对应内容

                Metas
                ---------------
                in :delta
                    default: 5
                    range: 5~50
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(
                1,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('volume'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

    class _UnRegister(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Observer, id, nameList)

        def temperature(self):
            """
                注销模块检测的温度值上传

                """
            unregister = _return_event_start(
                3,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('temperature'),
            )
            unregister._unregister()

        def humidity(self):
            """
                注销模块检测的湿度值上传

                """
            unregister = _return_event_start(
                2,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('humidity'),
            )
            unregister._unregister()

        def light(self):
            """
                注销模块检测的亮度值上传

                """
            unregister = _return_event_start(
                0,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('light'),
            )
            unregister._unregister()

        def volume(self):
            """
                注销模块检测的声音强度值上传

                """
            unregister = _return_event_start(
                1,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('volume'),
            )
            unregister._unregister()

    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['observer'])
        self._data_own = [0, 0, 0, 0]

        self._name_list = list()
        self.event = Observer._Event(id, self._name_list)
        self.register = Observer._Register(id, self._name_list)
        self.unregister = Observer._UnRegister(id, self._name_list)

    def _get_data(self, frame):
        
        
        temp = _DataFormat(['B', 'B', 'B', 'b'])
        self._data_own = temp.get_data_list(frame[4:])

        _set_event_value(self._name_list, self._data_own)

    def get_temperature(self):
        """
            获取温度值（°C）

            Parameters
            ----------

            Returns
            -------
            int
                温度值，范围 -20~100°C

            Metas
            ---------------
            out :
                range: -20~100°C
                
            Examples
            -------

            .. code-block:: python

                # 显示各种环境参数（温湿度，亮度音量），显示效果如下
                #   ----------------
                #     温度     湿度   
                #     亮度     音量   
                #   ----------------
                from wonderbits import Observer, Display
                display1 = Display()
                observer1 = Observer()

                while True:
                    display1.print(1, 1, observer1.get_temperature())
                    display1.print(1, 10, observer1.get_humidity())
                    display1.print(2, 1, observer1.get_light())
                    display1.print(2, 10, observer1.get_volume())

            """
        return self._data_own[3]

    def get_humidity(self):
        """
            获取湿度值(%RH）


            Parameters
            ----------

            Returns
            -------
            int
                湿度值，范围 0~100%RH

            Metas
            ---------------
            out :
                range: 0~100
                
            Examples
            -------
            未提供。可参考 `get_temperature`_ 的使用案例

            """
        return constrain(self._data_own[2], 0, 100)

    def get_light(self):
        """
            获取亮度值
            亮度值代表相对强度，值越大代表亮度越强

            Parameters
            ----------

            Returns
            -------
            int
                亮度值，范围 0~100

            Metas
            ---------------
            out :
                range: 0~100
                
            Examples
            -------
            未提供。可参考 `get_temperature`_ 的使用案例

            """
        return self._data_own[0]

    def get_volume(self):
        """
            获取声音强度值
            声音强度值代表相对强度，值越大代表声音越响

            Parameters
            ----------

            Returns
            -------
            int
                声音强度值，范围 0~100

            Metas
            ---------------
            out :
                range: 0~100
                
            Examples
            -------
            未提供。可参考 `get_temperature`_ 的使用案例

            .. code-block:: python
                
                # 绘制声音强度波形图
                from wonderbits import Observer, Display
                display1 = Display()
                observer1 = Observer()

                while True:
                    for x in range(1,121):
                        y = observer1.get_volume()/3
                        display1.draw_chart(x, y)


                

            """
        return self._data_own[1]
