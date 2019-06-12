# Display.py
"""
显示模块/Display
=============================
用于显示各种内容，包含数字，英文，中文等，还可以进行简单画图展示。
侧边的翻页按键，用于切换不同页的显示内容

"""

# from wb import DEVICE_TYPE
from public import DEVICE_TYPE
from wb import _TYPE_REQUEST
from wb import constrain
from wb import _DataFormat
from micropython import const
from ModuleObj import ModuleObj
from EventManager import EventNameList, _return_event_start, _set_event_value, EventManager

# BUTTON_NONE = 0
# BUTTON_L = 1
# BUTTON_R = 2
# BUTTON_M = 3
# BUTTON_ML = 4
# BUTTON_L = 0x02
# BUTTON_R = 0x04
# BUTTON_M = 0x08
# BUTTON_ML = 0x10

_CMD_OLED_BUTTON = const(0x08)  # OLED 按键使能
_CMD_OLED_Page = const(0x09)  # OLED 显示某页
_CMD_OLED_Clear = const(0x0A)  # OLED 清屏
_CMD_OLED_String = const(0x0B)  # OLED 显示字符串
_CMD_OLED_ClearRow = const(0x0C)  # OLED 清某一行
_CMD_OLED_TURN = const(0x0D)  # OLED 翻转屏幕
_CMD_OLED_ROLL = const(0x0E)  # OLED 控制滚条
_CMD_OLED_DOT = const(0x10)  # OLED画点
_CMD_OLED_LINE = const(0x11)  # OLED画线
_CMD_OLED_UPDATE = const(0x12)  # 自动更新显示设置
_CMD_OLED_REFRESH = const(0x13)  # 手动刷新显示命令

_DISPLAY_TIMEOUT = const(100)

_BUTTON_ENABLE = const(1)
_BUTTON_DISABLE = const(2)

_DIR_ROTATED = const(0)
_DIR_INITIAL = const(1)

_DRAW_NORMAL = const(0x00)
_DRAW_SAVED = const(0x01)

_COLOR_WHITE = const(0x00)
_COLOR_BLACK = const(0x01)


class Display(ModuleObj):
    BUTTON_NONE = const(0x01)
    """
    翻页按键未按下
    """
    BUTTON_L = const(0x02)
    """
    翻页按键拨到左侧
    """
    BUTTON_R = const(0x04)
    """
    翻页按键拨到右侧
    """
    BUTTON_M = const(0x08)
    """
    翻页按键拨到右侧
    """
    # BUTTON_ML = 0x10

    SIZE_SMALL = const(0x02)
    """
    小号字体
    """
    SIZE_BIG = const(0x04)
    """
    大号字体
    """

    class _Event(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Display, id, nameList)

        def button_left(self, interval=50):
            """
                当翻页按键向左拨动会执行事件修饰的函数

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

                    # 当翻页按键向左拨动时，执行函数function
                    @display1.event.button_left()
                    def function():
                        pass

                    # 修改检测周期为100ms,当翻页按键向左拨动时，执行函数function
                    @display1.event.button_left(100)
                    def function():
                        pass

                """
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('Left'),
                numFlag=Display.BUTTON_L)
            return event._compare(EventManager._FALSE_TO_TRUE_ACTION, None,
                                  interval)

        def button_right(self, interval=50):
            """
                当翻页按键向右拨动会执行事件修饰的函数

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

                    # 当翻页按键向右拨动时，执行函数function
                    @display1.event.button_right()
                    def function():
                        pass

                    # 修改检测周期为100ms,当翻页按键向右拨动时，执行函数function
                    @display1.event.button_right(100)
                    def function():
                        pass

                """
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('Right'),
                numFlag=Display.BUTTON_R)
            return event._compare(EventManager._FALSE_TO_TRUE_ACTION, None,
                                  interval)

        def button_pressed(self, interval=50):
            """
                当翻页按键按下会执行事件修饰的函数

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

                    # 当翻页按键按下时，执行函数function
                    @display1.event.button_pressed()
                    def function():
                        pass

                    # 修改检测周期为100ms,当翻页按键按下时，执行函数function
                    @display1.event.button_pressed(100)
                    def function():
                        pass

                """
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('Press'),
                numFlag=Display.BUTTON_M | 0x10)
            return event._compare(EventManager._FALSE_TO_TRUE_ACTION, None,
                                  interval)

        # def buttonLongPressed(self, interval=50):
        #     event = _return_event_start(
        #         0,
        #         EventManager._BOOL_VALUE_TYPE,
        #         self.get_name('LPress'),
        #         numFlag=Display.BUTTON_ML)
        #     return event._compare(EventManager._FALSE_TO_TRUE_ACTION, None,
        #                              interval)

        def button_released(self, interval=50):
            """
                当翻页按键松开会执行事件修饰的函数

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

                    # 当翻页按键松开时，执行函数function
                    @display1.event.button_released()
                    def function():
                        pass

                    # 修改检测周期为100ms,当翻页按键松开时，执行函数function
                    @display1.event.button_released(100)
                    def function():
                        pass

                """
            event = _return_event_start(
                0,
                EventManager._BOOL_VALUE_TYPE,
                self.get_name('Release'),
                numFlag=0x1E)
            return event._compare(EventManager._TRUE_TO_FALSE_ACTION, None,
                                  interval)

    class _Register(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Display, id, nameList)

        def button(self, interval=50):
            """
                注册翻页按键值上传，当翻页按键状态改变会触发事件并接收到数据，返回类型为int

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

                .. code-block:: python

                    # 注册翻页按键值上传
                    display1.register.button()

                    # 注册翻页按键值上传,并修改检测周期
                    display1.register.button(100)

                当满足触发条件时返回 
                ``{"type":"event","module":"display1","source":"button","value":"2"}``

                """
            register = _return_event_start(0, EventManager._NUMBER_VALUE_TYPE,
                                           self.get_name('button'))
            register._register(EventManager._CHANGED_ACTION, 1, interval)

    class _UnRegister(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, Display, id, nameList)

        def button(self):
            """
                注销翻页按键值上传

                Examples
                -------

                .. code-block:: python

                    # 注销按键状态上传
                    display1.unregister.button()
                
                """
            unregister = _return_event_start(0,
                                             EventManager._NUMBER_VALUE_TYPE,
                                             self.get_name('button'))
            unregister._unregister()

    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['display'])
        self._name_list = list()

        self._X = 1
        self._Y = 1
        self._data_own = [1]
        self._chart_x = [None for i in range(8)]
        self._chart_y = [None for i in range(8)]

        self.event = self._Event(id, self._name_list)
        self.register = self._Register(id, self._name_list)
        self.unregister = self._UnRegister(id, self._name_list)

    def _get_data(self, frame):

        temp = _DataFormat('B')
        value = temp.get_data_list(frame[4:])[0]
        # print(frame[4], value, 'end')
        self._data_own[0] = 0x01 << value if value < 4 else 0x08

        _set_event_value(self._name_list, self._data_own)

    def print(self, row, column, text, size=SIZE_SMALL):
        """
            在某个位置显示内容

            Parameters
            ----------
            row : int
                显示行数：1~16
            column : int
                显示列数：1~15
            text : str
                显示内容，可以是字符串，整数，小数
            size : int
                设置显示的大小，默认为小号字体
                SIZE_SMALL：小号字体，值为2
                SIZE_BIG：大号字体（不支持汉字），值为4

            Metas
            ---------------
            in :row
                range: 1~16
            in :column
                range: 1~15
            in :size
                default:0x02
                SIZE_SMALL:0x02
                SIZE_BIG:0x04

            Examples
            -------
            
            .. code-block:: python

                # 显示各种不同内容
                from wonderbits import Display
                display1 = Display()

            
                # 在第1行第1列显示字符串 'Hello'
                display1.print(1, 1, 'Hello')

                # 在第1行第10列显示浮点型数字 -3.14
                display1.print(1, 10, -3.14)

                # 在第2行第1列显示变量
                temp = 10
                temp = temp + 3
                display1.print(2, 1, temp)
                
                # 在大字模式的第2行第1列显示 'big'
                display1.print(2, 1, 'big', Display.SIZE_BIG)

            """
        # uart2.write('a')
        if isinstance(text, float):
            text = round(text, 2)
        if not isinstance(text, str):
            text = str(text) + ' '

        # uart2.write('b')
        temp = _DataFormat('BBBBBBS')
        # uart2.write('c')
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list(
                [_CMD_OLED_String, column, row,
                 len(text), size, 1, text]))
        del text
        # uart2.write('e')

    def draw_dot(self, x, y, page=1):
        """
            在指定坐标画一个点
            在画点的页使用print函数会导致已经画过的点消失
            切换到不同的页码在回到画点的页码也会导致已经画过的点消失

            Parameters
            ----------
            x : int
                X轴坐标：1~119
            y : int
                Y轴坐标：1~32
            page : int
                显示页数：1~8
                默认第1页

            Metas
            ---------------
            in :x
                range: 1~119
            in :y
                range: 1~32
            in :page
                default: 1
                range: 1~8

            Examples
            -------

            .. code-block:: python
                
                # 在屏幕上画一条直线(y=x/4)上的点集合
                from wonderbits import Display
                display1 = Display()

                for x in range(1, 119):
                    display1.draw_dot(x, x/4) 
            
            """
        x = constrain(x, 1, 119)
        y = constrain(y, 1, 32)
        temp = _DataFormat('BBBBBBBB')
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list([
                _CMD_OLED_DOT, x, 33 - y, 0, 0, page, _DRAW_NORMAL,
                _COLOR_BLACK
            ]))

    def draw_line(self, head_x, head_y, tail_x, tail_y, page=1):
        """
            通过给定坐标画线段
            在画线的页使用print函数会导致已经画过的线消失
            切换到不同的页码在回到画线的页码也会导致已经画过的线消失

            Parameters
            ----------
            head_x : int
                起始点X轴坐标：1~119
            head_y : int
                起始点Y轴坐标：1~32
            tail_x : int
                终止点X轴坐标：1~119
            tail_y : int
                终止点Y轴坐标：1~32
            page : int
                显示页数：1~8
                默认第1页
            
            Metas
            ---------------
            in :head_x
                range: 1~119
            in :head_y
                range: 1~32
            in :tail_x
                range: 1~119
            in :tail_y
                range: 1~32
            in :page
                default: 1
                range: 1~8

            Examples
            -------

            .. code-block:: python
                
                # 在屏幕上画两条线，将屏幕分为四份
                from wonderbits import Display
                display1 = Display()

                # 在第1页以 (1, 16) 为起点， (119, 16) 为终点画一条直线
                display1.draw_line(1, 16, 119, 16)
            
                # 在第1页以 (60, 1) 为起点， (60, 32) 为终点画一条直线
                display1.draw_line(60, 1, 60, 32)

            """

        head_x = constrain(head_x, 1, 119)
        head_y = constrain(head_y, 1, 32)
        tail_x = constrain(tail_x, 1, 119)
        tail_y = constrain(tail_y, 1, 32)
        temp = _DataFormat('BBBBBBBB')
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list([
                _CMD_OLED_LINE, head_x, 33 - head_y, tail_x, 33 - tail_y, page,
                _DRAW_NORMAL, _COLOR_BLACK
            ]))

    def draw_chart(self, x, y, page=1):
        """
            画折线图
            以上次传入的坐标为起点，本次坐标为终点画线段。如果是首次使用，则只画单个点

            Parameters
            ----------
            x : int
                X轴坐标：1~119
            y : int
                Y轴坐标：1~32
            page : int
                显示页数：1~8
                默认画点在第1页
            
            Metas
            ---------------
            in :x
                range: 1~119
            in :y
                range: 1~32
            in :page
                default: 1
                range: 1~8
            
            Examples
            -------
            
            .. code-block:: python
               
                # 根据坐标画一组折线
                from wonderbits import Display
                display1 = Display()

                # 定义一堆点坐标
                dots =[(1,20),(5,30),(10,5),(15,40),(25,1)]

                # 将所有点取出来画折线
                for dot in dots:
                    display1.draw_chart(dot[0],dot[1])

            .. code-block:: python
            
                # 显示动态心电图
                from wonderbits import Display
                display1 = Display()

            """
        page = page - 1
        if self._chart_x[page] == None or self._chart_y[page] == None:
            self._chart_x[page] = x
            self._chart_y[page] = y
        self.draw_line(self._chart_x[page], self._chart_y[page], x, y,
                       page + 1)
        self._chart_x[page] = x
        self._chart_y[page] = y

    def turn_to_page(self, page):
        """
            转到某页

            Parameters
            ----------
            page : int
                页码：1~8

            Metas
            ---------------
            in :page
                range: 1~8

            Examples
            -------
            
            .. code-block:: python

                # 转到某页查看内容
                from wonderbits import Display
                import time
                display1 = Display()

                display1.print(1,1,'Page1 test') # 在第1页显示'Page1 test'
                display1.print(3,1,'this is Page2') # 在第2页(每页只能显示2行，所以第3行就是在第2页了)显示'this is Page2'

                while True:
                    # 转到第2页查看显示内容
                    display1.turn_to_page(2)
                    time.sleep(2) # 等待2秒

                    # 转到第1页查看显示内容
                    display1.turn_to_page(1)
                    time.sleep(2) # 等待2秒
            """
        page = constrain(page, 1, 8)
        temp = _DataFormat('BB')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_OLED_Page, page - 1]))

    def clear_page(self, page=1):
        """
            清除某页显示的内容

            Parameters
            ----------
            page : int
                清除的页码：1~8
                默认第1页

            Metas
            ---------------
            in :page
                default: 1
                range: 1~8
                
            Examples
            -------

            .. code-block:: python
                
                # 清除某页显示内容
                from wonderbits import Display
                display1 = Display()

                display1.print(1,1,'somthing...')
               
                # 清除第1页
                display1.clear_page(1)

                display1.print(2,1,'clear')
                # 观察实验效果,你会发现'something...'闪一下就消失了
                # 只剩'clear',因为之前的内容被清除了

            """
        page = constrain(page, 1, 8) - 1
        temp = _DataFormat('BB')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_OLED_ClearRow, page]))
        self._chart_x[page] = None
        self._chart_y[page] = None

    def clear_all_pages(self, block=False):
        """
            清除全部8页显示的内容

            Parameters
            ----------
            block : bool
                阻塞参数：
                False: 不阻塞
                True: 阻塞
                
            Metas
            ---------------
            in :block
                default: False

            Examples
            -------

            .. code-block:: python

                # 清除所有显示内容
                from wonderbits import Display
                display1 = Display()

                # 在清除之前显示一些文字
                display1.print(1,1,'somthing1...')
                display1.print(3,1,'somthing2...')
                display1.print(5,1,'somthing3...')
               
                # 清除第1页
                display1.clear_all_pages()

                display1.print(2,1,'clear')
                # 观察实验效果你会发现只剩'clear',因为之前的内容被清除了

            """
        self._X = 1
        self._Y = 1
        temp = _DataFormat('B')
        if block:
            self._send_with_ack(_TYPE_REQUEST, temp.get_list(
                [_CMD_OLED_Clear]), _DISPLAY_TIMEOUT)
        else:
            self._send_without_ack(_TYPE_REQUEST,
                                   temp.get_list([_CMD_OLED_Clear]))
        for i in range(8):
            self._chart_x[i] = None
            self._chart_y[i] = None

    def disable_page_turning(self):
        """
            禁止翻页按键功能
            禁止翻页按键功能后将不能通过翻页按键来切换不同页码的显示内容
            系统默认开启翻页按键功能

            Examples
            -------
            未提供。可参考 `get_button_state`_ 的使用案例

            """
        temp = _DataFormat('BB')
        self._send_without_ack(
            _TYPE_REQUEST, temp.get_list([_CMD_OLED_BUTTON, _BUTTON_DISABLE]))

    def enable_page_turning(self):
        """
            开启翻页按键功能
            系统默认开启翻页按键功能

            Examples
            -------
            
            .. code-block:: python

                # 开启翻页按键功能
                from wonderbits import Display
                display1 = Display()
                
                # 开启翻页按键功能
                display1.enable_page_turning()

            """
        temp = _DataFormat('BB')
        self._send_without_ack(
            _TYPE_REQUEST, temp.get_list([_CMD_OLED_BUTTON, _BUTTON_ENABLE]))

    def get_button_state(self):
        """
            获取翻页按钮状态

            Parameters
            ----------


            Returns
            -------
            int
                翻页按钮状态
                BUTTON_NONE：没有按键按下，值为1
                BUTTON_L：左键按下，值为2 
                BUTTON_R：右键按下，值为4 
                BUTTON_M：中键按下，值为8
                

            Metas
            ---------------
            out :
                BUTTON_NONE = 0x01
                BUTTON_L = 0x02
                BUTTON_R = 0x04
                BUTTON_M = 0x08

            Examples
            -------

            .. code-block:: python
                
                # 实时显示翻页按钮状态
                from wonderbits import Display
                display1 = Display()
                
                # 先禁止翻页功能，否则按钮拨动时会翻页显示
                display1.disable_page_turning()

                # 实时显示状态值
                while True:
                    display1.print(1, 1, display1.get_button_state())

            """
        return (self._data_own[0] & 0x1F)

    def _set_direction(self, dir):
        temp = _DataFormat('BB')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_OLED_TURN, dir]))

    def set_direction_reverse(self):
        """
            设置显示方向为翻转显示方向，使用该函数后显示内容将会进行180°翻转

            Examples
            -------

            .. code-block:: python

                # 通过按钮控制翻转显示
                from wonderbits import Display
                display1 = Display()
                
                # 先禁止翻页功能，否则按钮拨动时会翻页显示
                display1.disable_page_turning()

                display1.print(1, 1, 'TEST 123')
                
                # 实时监测翻页按钮状态,向左拨动时翻转显示，向右拨动时正常显示
                while True:
                    if display1.get_button_state() == 2:
                        display1.set_direction_reverse()

                    if display1.get_button_state() == 4:
                        display1.set_direction_regular()

            """
        self._set_direction(_DIR_ROTATED)

    def set_direction_regular(self):
        """
            设置显示方向为系统默认显示方向

            Examples
            -------
            未提供。可参考 `set_direction_reverse`_ 的使用案例

            """
        self._set_direction(_DIR_INITIAL)

    def hide_scrollbar(self):
        """
            隐藏页码滚动指示条（屏幕右边的白色小点，用于指示当前页码）
            系统默认显示页码滚动指示条
            隐藏后每行最大显示字符数由15变为16

            Examples
            -------

            .. code-block:: python

                # 通过按钮控制是否显示页码指示条
                from wonderbits import Display
                display1 = Display()
                
                # 先禁止翻页功能，否则按钮拨动时会翻页显示
                display1.disable_page_turning()
                
                # 实时监测翻页按钮状态,向左拨动时隐藏页码指示条，向右拨动时显示页码指示条，并显示16个字符内容
                while True:
                    if display1.get_button_state() == 2:
                        display1.hide_scrollbar()
                        display1.print(1, 1, '0123456789abcdef')

                    if display1.get_button_state() == 4:
                        display1.show_scrollbar()
                        display1.print(1, 1, '0123456789abcdef')

            """
        temp = _DataFormat('BB')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_OLED_ROLL, 1]))

    def show_scrollbar(self):
        """
            显示页码滚动指示条
            系统默认显示页码滚动指示条

            Examples
            -------
            未提供。可参考 `hide_scrollbar`_ 的使用案例

            """
        temp = _DataFormat('BB')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_OLED_ROLL, 0]))

    def _set_coordinate(self, row, column):
        """
            设定显示位置
            设定显示位置后，直接使用跟随显示将在设定位置处开始显示内容

            Parameters
            ----------
            row : int
                显示行数：1~16
            column : int
                显示列数：1~15

            Metas
            ---------------
            in :row
                range: 1~16
            in :column
                range: 1~15
            
            Examples
            -------

            设定显示位置

            display1._set_coordinate(1, 1)

            """
        self._Y = row
        self._X = column

    def _set_update(self, key):
        temp = _DataFormat('BB')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_OLED_UPDATE, key]))

    def disable_auto_refresh(self):
        """
            禁止自动刷新显示功能
            禁止自动刷新后，只能调用刷新函数refresh() 才能改变显示内容
            系统默认开启自动刷新显示功能

            Examples
            -------

            .. code-block:: python

                # 通过按钮控制是否显示页码指示条
                from wonderbits import Display
                display1 = Display()

                # 先禁止翻页功能，否则按钮拨动时会翻页显示
                display1.disable_page_turning()

                # 禁止自动刷新显示功能
                display1.disable_auto_refresh()

                # 使用print功能将不会再显示屏上出现'hello'
                display1.print(1, 1, 'hello')

                num = 0
                
                while True:
                    
                    # 在第2行持续刷新显示num的数值，num一直在增长
                    num = num + 1
                    display1.print(2, 1, num)
                    
                    if display1.get_button_state() == 2:
                        display1.disable_auto_refresh() # 再次确保关闭自动刷新功能
                        display1.refresh()

                    if display1.get_button_state() == 4:
                        display1.enable_auto_refresh()

                    # 实验现象应该是，当翻页按钮向左拨动时，每次拨动都会更新一次显示数字，不拨动时数字显示不会变化
                    # 当翻页按钮向右拨动后，数值会持续自己刷新

            """
        self._set_update(0)

    def enable_auto_refresh(self):
        """
            开启自动刷新显示功能
            系统默认开启自动刷新显示功能

            Examples
            -------
            未提供。可参考 `disable_auto_refresh`_ 的使用案例
            """
        self._set_update(1)

    def refresh(self):
        """
            更新一次显示内容
            在禁止自动刷新显示功能后只能靠此函数来更新显示内容
            系统默认开启自动刷新显示功能

            Examples
            -------
            未提供。可参考 `disable_auto_refresh`_ 的使用案例

            """
        temp = _DataFormat('B')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_OLED_REFRESH]))

    def draw_save_dot(self, x, y, page=1):
        """
            在指定坐标画一个点
            画点后始终存在，可以使用清屏擦除
            可与print在同一页显示，显示位置冲突时以画点内容为主

            Parameters
            ----------
            x : int
                X轴坐标：1~119
            y : int
                Y轴坐标：1~32
            page : int
                显示页数：1~8
                默认第1页

            Metas
            ---------------
            in :x
                range: 1~119
            in :y
                range: 1~32
            in :page
                default: 1
                range: 1~8

            Examples
            -------

            .. code-block:: python

                # 在屏幕上画一条直线(y=x/4)上的点集合
                from wonderbits import Display
                display1 = Display()

                for x in range(1, 119):
                    display1.draw_save_dot(x, x/4)

            """
        x = constrain(x, 1, 119)
        y = constrain(y, 1, 32)
        temp = _DataFormat('BBBBBBBB')
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list([
                _CMD_OLED_DOT, x, 33 - y, 0, 0, page, _DRAW_SAVED, _COLOR_BLACK
            ]))

    def draw_save_line(self, head_x, head_y, tail_x, tail_y, page=1):
        """
            通过给定坐标画线段
            画线后始终存在，可以使用清屏擦除
            可与print在同一页显示，显示位置冲突时以画线内容为主

            Parameters
            ----------
            head_x : int
                起始点X轴坐标：1~119
            head_y : int
                起始点Y轴坐标：1~32
            tail_x : int
                终止点X轴坐标：1~119
            tail_y : int
                终止点Y轴坐标：1~32
            page : int
                显示页数：1~8
                默认第1页

            Metas
            ---------------
            in :head_x
                range: 1~119
            in :head_y
                range: 1~32
            in :tail_x
                range: 1~119
            in :tail_y
                range: 1~32
            in :page
                default: 1
                range: 1~8

            Examples
            -------

            .. code-block:: python

                # 在屏幕上画两条线，将屏幕分为四份
                from wonderbits import Display
                display1 = Display()

                # 在第1页以 (1, 16) 为起点， (119, 16) 为终点画一条直线
                display1.draw_line(1, 16, 119, 16)

                # 在第1页以 (60, 1) 为起点， (60, 32) 为终点画一条直线
                display1.draw_line(60, 1, 60, 32)

            """

        head_x = constrain(head_x, 1, 119)
        head_y = constrain(head_y, 1, 32)
        tail_x = constrain(tail_x, 1, 119)
        tail_y = constrain(tail_y, 1, 32)
        temp = _DataFormat('BBBBBBBB')
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list([
                _CMD_OLED_LINE, head_x, 33 - head_y, tail_x, 33 - tail_y, page,
                _DRAW_SAVED, _COLOR_BLACK
            ]))

    def draw_save_chart(self, x, y, page=1):
        """
            画折线图
            以上次传入的坐标为起点，本次坐标为终点画线段。如果是首次使用，则只画单个点

            Parameters
            ----------
            x : int
                X轴坐标：1~119
            y : int
                Y轴坐标：1~32
            page : int
                显示页数：1~8
                默认画点在第1页

            Metas
            ---------------
            in :x
                range: 1~119
            in :y
                range: 1~32
            in :page
                default: 1
                range: 1~8

            Examples
            -------

            .. code-block:: python

                # 根据坐标画一组折线
                from wonderbits import Display
                display1 = Display()

                # 定义一堆点坐标
                dots =[(1,20),(5,30),(10,5),(15,40),(25,1)]

                # 将所有点取出来画折线
                for dot in dots:
                    display1.draw_chart(dot[0],dot[1])

            .. code-block:: python

                # 显示动态心电图
                from wonderbits import Display
                display1 = Display()

            """

        page = page - 1
        if self._chart_x[page] == None or self._chart_y[page] == None:
            self._chart_x[page] = x
            self._chart_y[page] = y
        self.draw_save_line(self._chart_x[page], self._chart_y[page], x, y,
                            page + 1)
        self._chart_x[page] = x
        self._chart_y[page] = y
