# LED.py
"""
灯带模块/LightBelt
=============================
此模块可以连接灯带使用，灯带是由许多LED灯组成的，用户可以根据需要裁剪合适的LED灯个数。
灯带模块可以控制每个LED灯的颜色，去实现一些酷炫的效果

"""
from public import DEVICE_TYPE, _TYPE_REQUEST
from ModuleObj import ModuleObj, constrain
from syspublic import Msg
from dataFormat import _DataFormat

_CMD_LightBelt_setColor = 0x08
_CMD_LightBelt_setLen = 0x09
_CMD_LightBelt_flash = 0x0A
_CMD_LightBelt_flashOff = 0x0B
_CMD_LightBelt_roll = 0x0C
_CMD_LightBelt_rollOff = 0x0D
_CMD_LightBelt_addColor = 0x0E
_CMD_LightBelt_setBrightness = 0x0F


class LightBelt(ModuleObj):
    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['lightBelt'])

    def set_leds_rgb(self, start, end, r, g, b):
        """
            设置一段LED灯颜色（r,g,b 参数都设置为0时，关闭LED）

            Parameters
            ----------
            start : int
                起始位置：1~100
            end : int
                结束位置：1~100
            r : int
                红色：0~255
            g : int
                绿色：0~255
            b : int
                蓝色：0~255

            Metas
            ---------------
            in :start
                range: 1~100
            in :end
                range: 1~100
            in :r
                range: 0~255
            in :g
                range: 0~255
            in :b
                range: 0~255

            Examples
            -------

            .. code-block:: python

                # 分段设置灯带为红色，绿色，蓝色。（本实验需要连接至少有10个LED灯的灯带）
                from wonderbits import LightBelt
                lightBelt1 = LightBelt()

                # 设置第1-3个为红色
                lightBelt1.set_leds_rgb(1, 3, 100, 0, 0)
                # 设置第4-6个为绿色
                lightBelt1.set_leds_rgb(4, 6, 0, 100, 0)
                # 设置第7-9个为蓝色
                lightBelt1.set_leds_rgb(7, 9, 0, 0, 100)

                # 设置第10个为黄色
                lightBelt1.set_leds_rgb(1, 3, 100, 100, 0)
 
            """
        r = constrain(r, 0, 255)
        g = constrain(g, 0, 255)
        b = constrain(b, 0, 255)
        start = constrain(start, 1, 100)
        end = constrain(end, 1, 100)
        if start > end:
            start, end = end, start
        temp = _DataFormat(['B', 'B', 'B', 'B', 'B', 'B'])
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list([_CMD_LightBelt_setColor, start - 1, end, g, r, b]))

    def set_single_led_rgb(self, num, r, g, b):
        """
            设置单个LED灯颜色（r,g,b 参数都设置为0时，关闭LED）

            Parameters
            ----------
            num : int
                灯的位置：1~100
            r : int
                红色：0~255
            g : int
                绿色：0~255
            b : int
                蓝色：0~255

            Metas
            ---------------
            in :num
                range: 1~100
            in :r
                range: 0~255
            in :g
                range: 0~255
            in :b
                range: 0~255

            Examples
            -------

            .. code-block:: python

                # 控制每个灯为蓝色，且蓝色越来越亮。（本实验需要连接至少有10个LED灯的灯带）
                from wonderbits import LightBelt
                lightBelt1 = LightBelt()

                for b in range(1, 11):
                # 在这个循环里，b会从1变到10
                # 每次设置第b个灯的颜色为（0, 0, b*20）
                lightBelt1.set_single_led_rgb(b, 0, 0, b*20)
            """
        self.set_leds_rgb(num, num, r, g, b)
