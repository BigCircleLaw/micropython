# Acceleration.py
"""
加速度模块/Acceleration
=============================
加速度传感器可以测量空间X，Y，Z轴的加速度/角加速度等物理参数。运用简单的数学知识还可以计算出倾角等其他有意义的数值。

**常见应用场景**

- 加速度检测：睡眠质量监测，拍手检测（震动），姿态检测等
- 倾角感应：倾斜控制器，检测物品是否水平等
"""

from public import DEVICE_TYPE, _TYPE_REQUEST, RGB_Y, RGB_B
from ModuleObj import ModuleObj
from syspublic import Msg
from dataFormat import _DataFormat
from EventManager import EventNameList, _return_event_start, _set_event_value, EventManager

_CMD_ACC_Calibration = 0x08

_SPACE_X = 0
_SPACE_Y = 1
_SPACE_Z = 2


class Acceleration(ModuleObj):
    class _Event(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Acceleration, id, nameList)

        def x_acceleration_changed(self, delta=1, interval=50):
            """
                当加速度传感器检测的x轴加速度值发生改变时会执行事件修饰的函数

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
                                        self.get_name('x_acceleration'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def y_acceleration_changed(self, delta=1, interval=50):
            """
                当加速度传感器检测的y轴加速度值发生改变时会执行事件修饰的函数

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
            event = _return_event_start(1, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('y_acceleration'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def z_acceleration_changed(self, delta=1, interval=50):
            """
                当加速度传感器检测的z轴加速度值发生改变时会执行事件修饰的函数

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
                                        self.get_name('z_acceleration'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def acceleration_changed(self, delta=1, interval=50):
            """
                当加速度传感器检测的x、y、z三轴合加速度值发生改变时会执行事件修饰的函数

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
            event = _return_event_start(6, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('acceleration'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def x_angular_velocity_changed(self, delta=100, interval=50):
            """
                当加速度传感器检测的x轴角速度值发生改变时会执行事件修饰的函数

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
                    range: 50~500
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(3, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('x_angular_velocity'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def y_angular_velocity_changed(self, delta=100, interval=50):
            """
                当加速度传感器检测的y轴角速度值发生改变时会执行事件修饰的函数

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
                    range: 50~500
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(4, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('y_angular_velocity'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def z_angular_velocity_changed(self, delta=100, interval=50):
            """
                当加速度传感器检测的y轴角速度值发生改变时会执行事件修饰的函数

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
                    range: 50~500
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(5, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('z_angular_velocity'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

    class _Register(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Acceleration, id, nameList)

        def x_acceleration(self, delta=1, interval=50):
            """
                注册加速度传感器检测的x轴加速度值上传，当加速度传感器检测的x轴加速度值改变会接收到数据，返回类型为float

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
                self.get_name('x_acceleration'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def y_acceleration(self, delta=1, interval=50):
            """
                注册加速度传感器检测的y轴加速度值上传，当加速度传感器检测的y轴加速度值改变会接收到数据，返回类型为float

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
                1,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('y_acceleration'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def z_acceleration(self, delta=1, interval=50):
            """
                注册加速度传感器检测的z轴加速度值上传，当加速度传感器检测的z轴加速度值改变会接收到数据，返回类型为float

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
                self.get_name('z_acceleration'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def acceleration(self, delta=1, interval=50):
            """
                注册加速度传感器检测的x、y、z三轴合加速度值上传，当加速度传感器检测的x、y、z三轴合加速度值改变会接收到数据，返回类型为float

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
                6,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('acceleration'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def x_angular_velocity(self, delta=100, interval=50):
            """
                注册加速度传感器检测的x轴角速度值上传，当加速度传感器检测的x轴角速度值改变会接收到数据，返回类型为float

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
                    range: 50~500
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(
                3,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('x_angular_velocity'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def y_angular_velocity(self, delta=100, interval=50):
            """
                注册加速度传感器检测的y轴角速度值上传，当加速度传感器检测的y轴角速度值改变会接收到数据，返回类型为float

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
                    range: 50~500
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(
                4,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('y_angular_velocity'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def z_angular_velocity(self, delta=100, interval=50):
            """
                注册加速度传感器检测的z轴角速度值上传，当加速度传感器检测的z轴角速度值改变会接收到数据，返回类型为float

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
                    range: 50~500
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(
                5,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('z_angular_velocity'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

    class _UnRegister(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Acceleration, id, nameList)

        def x_acceleration(self):
            """
                注销加速度传感器检测的x轴加速度值上传

                """
            unregister = _return_event_start(
                0,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('x_acceleration'),
            )
            unregister._unregister()

        def y_acceleration(self):
            """
                注销加速度传感器检测的y轴加速度值上传

                """
            unregister = _return_event_start(
                1,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('y_acceleration'),
            )
            unregister._unregister()

        def z_acceleration(self):
            """
                注销加速度传感器检测的Z轴加速度值上传

                """
            unregister = _return_event_start(
                2,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('z_acceleration'),
            )
            unregister._unregister()

        def acceleration(self):
            """
                注销加速度传感器检测的x、y、z轴合加速度值上传

                """
            unregister = _return_event_start(
                6,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('acceleration'),
            )
            unregister._unregister()

        def x_angular_velocity(self):
            """
                注销加速度传感器检测的x轴角速度值上传

                """
            unregister = _return_event_start(
                3,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('x_angular_velocity'),
            )
            unregister._unregister()

        def y_angular_velocity(self):
            """
                注销加速度传感器检测的y轴角速度值上传

                """
            unregister = _return_event_start(
                4,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('y_angular_velocity'),
            )
            unregister._unregister()

        def z_angular_velocity(self):
            """
                注销加速度传感器检测的z轴角速度值上传

                """
            unregister = _return_event_start(
                5,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('z_angular_velocity'),
            )
            unregister._unregister()

    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['acceleration'])
        self._data_own = [0, 0, 0, 0, 0, 0, 0]

        self._name_list = list()
        self.event = Acceleration._Event(id, self._name_list)
        self.register = Acceleration._Register(id, self._name_list)
        self.unregister = Acceleration._UnRegister(id, self._name_list)

    def _get_data(self, frame):
        from math import sqrt
        
        
        temp = _DataFormat(['h', 'h', 'h', 'h', 'h', 'h'])
        self._data_own[:6] = temp.get_data_list(frame[4:])
        for i in range(3):
            self._data_own[i] = round(self._data_own[i] / 409.6, 2)
        for i in range(3, 6):
            self._data_own[i] = round(self._data_own[i] / 32.768, 2)
        self._data_own[6] = round(
            sqrt(self._data_own[_SPACE_X] * self._data_own[_SPACE_X] +
                 self._data_own[_SPACE_Y] * self._data_own[_SPACE_Y] +
                 self._data_own[_SPACE_Z] * self._data_own[_SPACE_Z]), 2)

        _set_event_value(self._name_list, self._data_own)

    def get_x_acceleration(self):
        """
            获取x轴加速度值，单位 m/s\ :sup:`2`


            Parameters
            ----------

            Returns
            -------
            float
                x轴加速度值，范围 -80~80 m/s\ :sup:`2`

            Metas
            ---------------
            out :
                range: -80~80
                
            Examples 
            -------

            .. code-block:: python
                
                # 加速度值显示案例

                from wonderbits import Acceleration,Display
                display1 = Display()
                acceleration1 = Acceleration()

                # 在显示屏上实时显示x轴加速度值
                while True:
                    display1.print(1, 1, acceleration1.get_x_acceleration())

            """
        return self._data_own[_SPACE_X]

    def get_y_acceleration(self):
        """
            获取y轴加速度值，单位 m/s\ :sup:`2`


            Parameters
            ----------

            Returns
            -------
            float
                y轴加速度值，范围 -80~80 m/s\ :sup:`2`

            Metas
            ---------------
            out :
                range: -80~80
                
            Examples
            -------
            未提供。可以参考 `get_x_acceleration`_ 的使用案例

            """
        return self._data_own[_SPACE_Y]

    def get_z_acceleration(self):
        """
            获取z轴加速度值，单位 m/s\ :sup:`2`


            Parameters
            ----------

            Returns
            -------
            float
                z轴加速度值，范围 -80~80 m/s\ :sup:`2`

            Metas
            ---------------
            out :
                range: -80~80
                
            Examples
            -------
            未提供。可以参考 `get_x_acceleration`_ 的使用案例

            """
        return self._data_own[_SPACE_Z]

    def get_acceleration(self):
        """
            获取x、y、z轴合加速度值，单位 m/s\ :sup:`2`
                

            Parameters
            ----------

            Returns
            -------
            float
                合加速度，范围-80~80 m/s\ :sup:`2`

            Metas
            ---------------
            out :
                range: -80~80
                
            Examples
            -------
            未提供。可以参考 `get_x_acceleration`_ 的使用案例

            """
        return self._data_own[6]

    def get_x_angular_velocity(self):
        """
            获取x轴角速度值，单位 °/s

            Parameters
            ----------

            Returns
            -------
            float
                x轴角速度值，范围-1000~1000 °/s

            Metas
            ---------------
            out :
                range: -1000~1000
                
            Examples
            -------

            .. code-block:: python

                # 角速度值显示案例
                from wonderbits import Acceleration,Display
                display1 = Display()
                acceleration1 = Acceleration()

                # 在显示屏上实时显示x轴角速度值
                while True:
                    display1.print(1, 1, acceleration1.get_x_angular_velocity())

            """
        return self._data_own[3]

    def get_y_angular_velocity(self):
        """
            获取y轴角速度值，单位 °/s

            Parameters
            ----------

            Returns
            -------
            float
                y轴角速度值，范围-1000~1000 °/s

            Metas
            ---------------
            out :
                range: -1000~1000
                
            Examples
            -------
            未提供。可以参考 `get_x_angular_velocity`_ 的使用案例


            """
        return self._data_own[4]

    def get_z_angular_velocity(self):
        """
            获取z轴角速度值，单位 °/s

            Parameters
            ----------

            Returns
            -------
            float
                z轴角速度值，范围-1000~1000 °/s

            Metas
            ---------------
            out :
                range: -1000~1000
                
            Examples
            -------

            未提供。可以参考 `get_x_angular_velocity`_ 的使用案例

            """
        return self._data_own[5]


# 这样存在风险，但是已经是定死的模板了，比如模块的灯不是蓝色时，使用了校准函数，在校准结束后会把等变为蓝色。

    def calibrate(self, block=True):
        """
            校准加速度传感器
            **注意**：校准过程中需确保加速度模块且保持静止不动，有汉字的一面朝上。
            校准时，模块指示灯会变为黄色，等待指示灯变蓝说明校准完成了。
                
            Parameters
            ----------
            block : bool
                阻塞参数：
                False表示不阻塞
                True表示阻塞

            Metas
            ---------------
            in :block
                default: True

            Examples
            -------

            .. code-block:: python

                # 加速度模块校准
                from wonderbits import Acceleration, Display
                acceleration1 = Acceleration()

                display1.print(1,1,'calibrating..')
                
                # 校准加速度传感器，校准时水平放在桌子上，观察模块上的指示灯变化
                acceleration1.calibrate()
                
                display1.print(1,1,'calibrated.  ')
            """
        self.set_onboard_rgb(RGB_Y)
        temp = _DataFormat(['B'])
        if block:
            self._send_with_ack(_TYPE_REQUEST,
                                temp.get_list([_CMD_ACC_Calibration]), 3000)
        else:
            self._send_without_ack(_TYPE_REQUEST,
                                   temp.get_list([_CMD_ACC_Calibration]))
        self.set_onboard_rgb(RGB_B)
