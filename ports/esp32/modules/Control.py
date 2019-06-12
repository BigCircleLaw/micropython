# Control.py
"""
控制模块/Control
=============================
本模块包含一系列可用于 **输入** 的传感器，用户可以通过传感器向电子系统发送指令进行“控制”。

按键：SW1、SW2
拨动开关：SW3
圆盘电阻器：SW4
阻抗传感器：M1、M2

"""

import time
from public import DEVICE_TYPE
from wb import _TYPE_REQUEST
from ModuleObj import ModuleObj
from wb import constrain

from wb import _DataFormat
from EventManager import EventNameList, _return_event_start, _set_event_value, EventManager

_CMD_SET_MAKEY = 0x0B  # 设置makey检测幅度


class Control(ModuleObj):

    _SW3_LEFT = 0x01  # 按键模块拨位左
    _SW3_RIGHT = 0x02  # 按键模块拨位右

    _SW1 = 0x04  # 按键模块按键1
    _SW2 = 0x08  # 按键模块按键2
    _M1 = 0x10  # 按键模块触摸按键1
    _M2 = 0x20  # 按键模块触摸按键2

    class _Event(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Control, id, nameList)

        def sw1_pressed(self, interval=50):
            """
                当按键sw1按下时会执行事件修饰的函数

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------

                .. code-block:: python

                    # 当按键sw1按下时，执行函数function
                    @display1.event.sw1_pressed()
                    def function():
                        pass

                    # 修改检测周期为100ms,当按键sw1按下时，执行函数function
                    @display1.event.sw1_pressed(100)
                    def function():
                        pass

                """
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw1'),
                numFlag=Control._SW1)
            return event._compare(EventManager._FALSE_TO_TRUE_ACTION, None,
                                  interval)

        def sw1_released(self, interval=50):
            """
                当按键sw1按下后放手时会执行事件修饰的函数

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------

                .. code-block:: python

                    # 当按键sw1按下后放手时，执行函数function
                    @display1.event.sw1_released()
                    def function():
                        pass

                    # 修改检测周期为100ms,当按键sw1按下后放手时，执行函数function
                    @display1.event.sw1_released(100)
                    def function():
                        pass

                """
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw1'),
                numFlag=Control._SW1)
            return event._compare(EventManager._TRUE_TO_FALSE_ACTION, None,
                                  interval)

        def sw2_pressed(self, interval=50):
            """
                当按键sw2按下时会执行事件修饰的函数

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------

                .. code-block:: python

                    # 当按键sw2按下时，执行函数function
                    @display1.event.sw2_pressed()
                    def function():
                        pass

                    # 修改检测周期为100ms,当按键sw2按下时，执行函数function
                    @display1.event.sw2_pressed(100)
                    def function():
                        pass

                """
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw2'),
                numFlag=Control._SW2)
            return event._compare(EventManager._FALSE_TO_TRUE_ACTION, None,
                                  interval)

        def sw2_released(self, interval=50):
            """
                当按键sw2按下后放手时会执行事件修饰的函数

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------

                .. code-block:: python

                    # 当按键sw2按下后放手时，执行函数function
                    @display1.event.sw2_released()
                    def function():
                        pass

                    # 修改检测周期为100ms,当按键sw2按下后放手时，执行函数function
                    @display1.event.sw2_released(100)
                    def function():
                        pass

                """
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw2'),
                numFlag=Control._SW2)
            return event._compare(EventManager._TRUE_TO_FALSE_ACTION, None,
                                  interval)

        def sw3_at_1(self, interval=50):
            """
                当开关sw3由0拨动到1时会执行事件修饰的函数

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------

                .. code-block:: python

                    # 当开关sw3由0拨动到1时，执行函数function
                    @display1.event.sw3_at_1()
                    def function():
                        pass

                    # 修改检测周期为100ms,当开关sw3由0拨动到1时，执行函数function
                    @display1.event.sw3_at_1(100)
                    def function():
                        pass

                """
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw3'),
                numFlag=Control._SW3_RIGHT)
            return event._compare(EventManager._FALSE_TO_TRUE_ACTION, None,
                                  interval)

        def sw3_at_0(self, interval=50):
            """
                当开关sw3由1拨动到0时会执行事件修饰的函数

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------

                .. code-block:: python

                    # 当开关sw3由1拨动到0时，执行函数function
                    @display1.event.sw3_at_0()
                    def function():
                        pass

                    # 修改检测周期为100ms,当开关sw3由1拨动到0时，执行函数function
                    @display1.event.sw3_at_0(100)
                    def function():
                        pass

                """
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw3'),
                numFlag=Control._SW3_LEFT)
            return event._compare(EventManager._FALSE_TO_TRUE_ACTION, None,
                                  interval)

        def sw4_changed(self, delta=1, interval=50):
            """
                当圆盘电阻器sw4的值发生改变时会执行事件修饰的函数

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
                    range: 1~50
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(1, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('sw4'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def m1_pressed(self, interval=50):
            """
                当触摸按键m1导通时会执行事件修饰的函数

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
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('m1'),
                numFlag=Control._M1)
            return event._compare(EventManager._FALSE_TO_TRUE_ACTION, None,
                                  interval)

        def m1_released(self, interval=50):
            """
                当触摸按键m1导通后放手时会执行事件修饰的函数

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
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('m1'),
                numFlag=Control._M1)
            return event._compare(EventManager._TRUE_TO_FALSE_ACTION, None,
                                  interval)

        def m2_pressed(self, interval=50):
            """
                当触摸按键m2导通时会执行事件修饰的函数

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
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('m2'),
                numFlag=Control._M2)
            return event._compare(EventManager._FALSE_TO_TRUE_ACTION, None,
                                  interval)

        def m2_released(self, interval=50):
            """
                当触摸按键m2导通后放手时会执行事件修饰的函数

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
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('m2'),
                numFlag=Control._M2)
            return event._compare(EventManager._TRUE_TO_FALSE_ACTION, None,
                                  interval)

        def m1_value_changed(self, delta=5, interval=50):
            """
                当触摸按键m1的电阻率发生改变时会执行事件修饰的函数

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
                    range: 1~50
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(2, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('m1Value'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

        def m2_value_changed(self, delta=5, interval=50):
            """
                当触摸按键m2的电阻率发生改变时会执行事件修饰的函数

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
                    range: 1~50
                in :interval
                    default: 50
                    range: 50~60000

                """
            event = _return_event_start(3, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('m2Value'))
            return event._compare(EventManager._CHANGED_ACTION, delta,
                                  interval)

    class _Register(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Control, id, nameList)

        def sw1(self, interval=50):
            """
                注册sw1值上传，当sw1状态改变会触发事件并接收到数据，返回类型为bool

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求，如果符合会发送对应内容

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------
                注册sw1值上传

                >>> control1.register.sw1()

                注册sw1值上传,并修改检测周期

                >>> control1.register.sw1(100)

                当满足触发条件时返回 

                ``{"type":"event","module":"control1","source":"sw1","value":"True"}``
                """
            register = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw1'),
                numFlag=Control._SW1)
            register._register(EventManager._CHANGED_ACTION, None, interval)

        def sw2(self, interval=50):
            """
                注册sw2值上传，当sw2状态改变会触发事件并接收到数据，返回类型为bool

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求，如果符合会发送对应内容

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------
                注册sw2值上传

                >>> control1.register.sw2()

                注册sw2值上传,并修改检测周期

                >>> control1.register.sw2(100)

                当满足触发条件时返回 

                ``{"type":"event","module":"control1","source":"sw2","value":"True"}``
                """
            register = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw2'),
                numFlag=Control._SW2)
            register._register(EventManager._CHANGED_ACTION, None, interval)

        def sw3(self, interval=50):
            """
                注册sw3值上传，当sw3状态改变会触发事件并接收到数据，返回类型为bool

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求，如果符合会发送对应内容

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------
                注册sw3值上传

                >>> control1.register.sw3()

                注册sw3值上传,并修改检测周期

                >>> control1.register.sw3(100)

                当满足触发条件时返回 

                ``{"type":"event","module":"control1","source":"sw3","value":"True"}``

                """
            register = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw3'),
                numFlag=Control._SW3_RIGHT)
            register._register(EventManager._CHANGED_ACTION, None, interval)

        def sw4(self, delta=1, interval=50):
            """
                注册sw4值上传，当sw4值改变会触发事件并接收到数据，返回类型为int

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
                    range: 1~50
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------
                注册sw4值上传

                >>> control1.register.sw4()

                注册sw4值上传,并修改触发上传的改变范围

                >>> control1.register.sw4(5)


                注册sw4值上传,并修改触发上传的改变范围和检测周期

                >>> control1.register.sw4(5, 100)

                当满足触发条件时返回 

                ``{"type":"event","module":"control1","source":"sw4","value":"50"}``
                """
            register = _return_event_start(
                1,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('sw4'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def m1(self, interval=50):
            """
                注册m1值上传，当m1状态改变会触发事件并接收到数据，返回类型为bool

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求，如果符合会发送对应内容

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------
                注册m1值上传

                >>> control1.register.m1()

                注册m1值上传,并修改检测周期

                >>> control1.register.m1(100)

                当满足触发条件时返回 

                ``{"type":"event","module":"control1","source":"m1","value":"True"}``
                """
            register = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('m1'),
                numFlag=Control._M1)
            register._register(EventManager._CHANGED_ACTION, None, interval)

        def m2(self, interval=50):
            """
                注册m2值上传，当m2状态改变会触发事件并接收到数据，返回类型为bool

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求，如果符合会发送对应内容

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------
                注册m2值上传

                >>> control1.register.m2()

                注册m2值上传,并修改检测周期

                >>> control1.register.m2(100)

                当满足触发条件时返回 

                ``{"type":"event","module":"control1","source":"m2","value":"True"}``
                """
            register = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('m2'),
                numFlag=Control._M2)
            register._register(EventManager._CHANGED_ACTION, None, interval)

        def m1_value(self, delta=5, interval=50):
            """
                注册m1电阻率值上传，当m1电阻率值改变会触发事件并接收到数据，返回类型为float

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
                    range: 1~50
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------
                注册m1Value值上传

                >>> control1.register.m1_value()

                注册m1Value值上传,并修改触发上传的改变范围

                >>> control1.register.m1_value(10)

                注册m1Value值上传,并修改触发上传的改变范围和检测周期

                >>> control1.register.m1_value(10, 100)

                当满足触发条件时返回 

                ``{"type":"event","module":"control1","source":"m1Value","value":"50"}``
                """
            register = _return_event_start(
                2,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('m1value'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

        def m2_value(self, delta=5, interval=50):
            """
                注册m2电阻率值上传，当m1电阻率值改变会触发事件并接收到数据，返回类型为float

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
                    range: 1~50
                in :interval
                    default: 50
                    range: 50~60000

                Examples
                -------
                注册m2Value值上传

                >>> control1.register.m2_value()

                注册m2Value值上传,并修改触发上传的改变范围

                >>> control1.register.m2_value(10)

                注册m2Value值上传,并修改触发上传的改变范围和检测周期

                >>> control1.register.m2_value(10, 100)

                当满足触发条件时返回 

                ``{"type":"event","module":"control1","source":"m2Value","value":"50"}``
                """
            register = _return_event_start(
                3,
                EventManager._NUMBER_VALUE_TYPE,
                self.get_name('m2value'),
            )
            register._register(EventManager._CHANGED_ACTION, delta, interval)

    class _UnRegister(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Control, id, nameList)

        def sw3(self):
            """
                注销sw3值上传

                Examples
                -------
                注销sw3值上传

                >>> control1.unregister.sw3()
                """
            unregister = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw3'),
                numFlag=Control._SW3_RIGHT)
            unregister._unregister()

        def sw1(self):
            """
                注销sw1值上传

                Examples
                -------
                注销sw1值上传

                >>> control1.unregister.sw1()
                """
            unregister = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw1'),
                numFlag=Control._SW1)
            unregister._unregister()

        def sw2(self):
            """
                注销sw2值上传

                Examples
                -------
                注销sw2值上传

                >>> control1.unregister.sw2()
                """
            unregister = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('sw2'),
                numFlag=Control._SW2)
            unregister._unregister()

        def m1(self):
            """
                注销m1值上传

                Examples
                -------
                注销m1值上传

                >>> control1.unregister.m1()
                """
            unregister = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('m1'),
                numFlag=Control._M1)
            unregister._unregister()

        def m2(self):
            """
                注销m2值上传

                Examples
                -------
                注销m2值上传

                >>> control1.unregister.m2()
                """
            unregister = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('m2'),
                numFlag=Control._M2)
            unregister._unregister()

        def sw4(self):
            """
                注销sw4值上传

                Examples
                -------
                注销sw4值上传

                >>> control1.unregister.sw4()
                """
            unregister = _return_event_start(1,
                                             EventManager._NUMBER_VALUE_TYPE,
                                             self.get_name('sw4'))
            unregister._unregister()

        def m1_value(self):
            """
                注销m1电阻率值上传

                Examples
                -------
                注销m1_value值上传

                >>> control1.unregister.m1_value()
                """
            unregister = _return_event_start(2,
                                             EventManager._NUMBER_VALUE_TYPE,
                                             self.get_name('m1Value'))
            unregister._unregister()

        def m2_value(self):
            """
                注销m2电阻率值上传

                Examples
                -------
                注销m2_value值上传

                >>> control1.unregister.m2_value()
                """
            unregister = _return_event_start(3,
                                             EventManager._NUMBER_VALUE_TYPE,
                                             self.get_name('m2Value'))
            unregister._unregister()

    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['control'])
        self._data_own = [0, 0, 0, 0]

        self._name_list = list()
        self.event = Control._Event(id, self._name_list)
        self.register = Control._Register(id, self._name_list)
        self.unregister = Control._UnRegister(id, self._name_list)

    def _get_data(self, frame):
        
        
        temp = _DataFormat('BBHH')
        self._data_own = temp.get_data_list(frame[4:])

        self._data_own[2] = round(self._data_own[2] / 10.04, 2)
        self._data_own[3] = round(self._data_own[3] / 10.04, 2)

        _set_event_value(self._name_list, self._data_own)

    def _do_update_value(self):
        pass

    def is_sw1_pressed(self):
        """
            判断按键SW1是否被按下

            Parameters
            ----------

            Returns
            -------
            bool
                True: 按键被按下
                False: 按键没有被按下

            Examples
            -------

            .. code-block:: python

                # 测试SW1和SW2状态，实时显示
 
                from wonderbits import Control,Display
                display1 = Display()
                control1 = Control()

                # 在显示屏上实时显示SW1和SW2的状态
                while True:
                    display1.print(1,1, control1.is_sw1_pressed() )
                    display1.print(2,1, control1.is_sw2_pressed() )

            """
        return (self._data_own[0] & self._SW1) != 0

    def is_sw2_pressed(self):
        """
            判断按键SW2是否被按下

            Parameters
            ----------

            Returns
            -------
            bool
                True: 按键按下
                False: 按键没有按下

            Examples
            -------
            未提供。可参考 `is_sw1_pressed`_ 的使用案例

            """
        return (self._data_own[0] & self._SW2) != 0

    def is_sw3_at_1(self):
        """
            判断SW3的是否在‘1’的位置（‘1’指的是电路上白色的数字）

            Parameters
            ----------

            Returns
            -------
            bool
                True: 开关SW3在'1'位置
                False: 开关SW3在'0'位置

            Examples
            -------
            
            .. code-block:: python

                # 测试SW1状态，实时显示
 
                from wonderbits import Control,Display
                display1 = Display()
                control1 = Control()

                # 在显示屏上实时显示SW1状态
                while True:
                    if control1.is_sw3_at_1():
                        display1.print(1,1,'left ')
                    else:
                        display1.print(1,1,'right')

            """
        if (self._data_own[0] & self._SW3_RIGHT) != 0:
            return True
        elif (self._data_own[0] & self._SW3_LEFT) != 0:
            return False
        else:
            print('Control not found')
            return None

    def get_sw4(self):
        """
            获取SW4的位置值

            Parameters
            ----------

            Returns
            -------
            int
                圆盘电阻器SW4的位置
                范围 0~100

            Metas
            ---------------
            out :
                range: 0~100
                
            Examples
            -------

            .. code-block:: python

                # 显示SW4位置值，并且当其大于50时显示‘>50 ’，否则显示'<=50'
 
                from wonderbits import Control,Display
                display1 = Display()
                control1 = Control()

                # 在显示屏上实时显示SW1状态
                while True:
                    value = control1.get_sw4() # 先获取SW4位置值，存在变量里
                    display1.print(1, 1, value) # 在显示屏第一行显示这个值
                    
                    # 通过判断这个变量的大小，分情况显示内容
                    if value > 50: 
                        display1.print(2,1,'>50 ')
                    else:
                        display1.print(2,1,'<=50')
            """
        if self._data_own[1] < 101:
            return self._data_own[1]
        return None

    def is_m1_connected(self):
        """
            判断获取M1与COM是否导通
            一般的使用方法是：将连接线插入到控制模块的接头上，实验者一手握住COM线头（黑色），另一手握住M1或M2线头（黄或绿色）。导通时板子上相应指示灯会亮起
            
            Parameters
            ----------

            Returns
            -------
            bool
                True: M1与COM之间导通(连接着可导通的介质，如：人体)
                False: M1与COM之间不导通
            Examples
            -------

            .. code-block:: python

                # 实时显示M1和COM之间是否导通
 
                from wonderbits import Control,Display
                display1 = Display()
                control1 = Control()

                # 当m1与com导通时显示'M1'，否则'No'
                while True:
                    if control1.is_m1_connected():
                        display1.print(1, 1, 'M1')
                    elif control1.is_m2_connected():
                        display1.print(1, 1, 'M2')
                    else:
                        display1.print(1, 1, 'No')
            """
        return (self._data_own[0] & self._M1) != 0

    def is_m2_connected(self):
        """
            判断获取M2与COM是否导通
            一般的使用方法是：将连接线插入到控制模块的接头上，实验者一手握住COM线头（黑色），另一手握住M1或M2线头（黄或绿色）。导通时板子上相应指示灯会亮起
            
            Parameters
            ----------

            Returns
            -------
            bool
                True: M2与COM之间导通(连接着可导通的介质，如：人体)
                False: M2与COM之间不导通            
            
            Examples
            -------
            未提供。可参考 `is_m1_connected`_ 的使用案例

            """
        return (self._data_own[0] & self._M2) != 0

    def set_m1_m2_sensitivity(self, limit):
        """
            设置M1和M2灵敏度
            灵敏度越高，is_m1_connected() 和is_m2_connected()越容易返回 True
            
            Parameters
            ----------
            limit : int
                灵敏度：0~100


            Metas
            ---------------
            in :limit
                range: 0~100

            Examples
            -------

            .. code-block:: python
                
                # 测试不同灵敏度的差别。当SW3位置在1时，灵敏度设为80；否则设置为20
                # 灵敏度越小，检测越不灵敏。所以设置为20，双手分别握住COM和M1，有可能检测不到导通状态，快去试试吧

                from wonderbits import Control,Display
                import time
                display1 = Display()
                control1 = Control()

                while True:
                    # 通过SW3的位置来设置不同的灵敏度
                    if control1.is_sw3_at_1():
                        control1.set_m1_m2_sensitivity(80)
                        display1.print(1, 1, 'set to 80.')
                    else:
                        control1.set_m1_m2_sensitivity(20)
                        display1.print(1, 1, 'set to 20.')

                    # 循环检测M1的状态并显示
                    if control1.is_m1_connected():
                        display1.print(2, 1, 'M1')
                    elif control1.is_m2_connected():
                        display1.print(2, 1, 'M2')
                    else:
                        display1.print(2, 1, 'No')   
            """
        limit = constrain(limit, 0, 100)
        temp = _DataFormat('BB')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_SET_MAKEY, limit]))

    def get_m1_value(self):
        """
            获取M1的电阻率

            Parameters
            ----------

            Returns
            -------
            float
                M1和COM之间的电阻率，值越大代表电阻越大。0代表短路，100代表绝缘
                范围 0~100

            Metas
            ---------------
            out :
                range: 0~100
                
            Examples
            -------
            
            .. code-block:: python

                # 实时显示M1的COM之间电阻率
                from wonderbits import Control,Display
                display1 = Display()
                control1 = Control()

                # 在显示屏上实时显示电阻率
                while True:
                    display1.print(1, 1, 'M1:')
                    display1.print(1, 4, control1.get_m1_value())
                    display1.print(2, 1, 'M2:')
                    display1.print(2, 4, control1.get_m2_value())
            
            """
        return self._data_own[2]

    def get_m2_value(self):
        """
            获取M2的电阻率

            Parameters
            ----------

            Returns
            -------
            float
                M2和COM之间的电阻率，值越大代表电阻越大。0代表短路，100代表绝缘
                范围 0~100


            Metas
            ---------------
            out :
                range: 0~100
                
            Examples
            -------
            未提供。可参考 `get_m1_value`_ 的使用案例

            """
        return self._data_own[3]
