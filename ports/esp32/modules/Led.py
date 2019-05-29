# LED.py
"""
彩灯模块/Led
=============================
LED彩色灯，可以通过设定红色（R）、绿色（G）、蓝色（B）的亮度来产生任意颜色的光。

"""

from public import DEVICE_TYPE, _TYPE_REQUEST
from ModuleObj import ModuleObj, constrain
from syspublic import Msg
from dataFormat import _DataFormat
from utime import sleep

_CMD_LED_Color = 0x08
_CMD_LED_Brightness = 0x09
_CMD_LED_Fade = 0x0A


class Led(ModuleObj):
    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['led'])
        self._r = 0
        self._g = 0
        self._b = 0

    def set_rgb(self, r, g, b):
        """
            设置彩灯颜色（r,g,b 参数都设置为0时，关闭LED）

            Parameters
            ----------
            r : int
                红色：0~255
            g : int
                绿色：0~255
            b : int
                蓝色：0~255

            Metas
            ---------------
            in :r
                range: 0~255
            in :g
                range: 0~255
            in :b
                range: 0~255

            Examples
            -------

            .. code-block:: python

                # 设置彩灯在红绿蓝之间变换5次，每个颜色持续0.5秒。最后关闭LED
                from wonderbits import Led
                import time
                led1 = Led()

                for i in range(5):
                    led1.set_rgb(10, 0, 0)
                    time.sleep(0.5)

                    led1.set_rgb(0, 10, 0)
                    time.sleep(0.5)

                    led1.set_rgb(0, 0, 10)
                    time.sleep(0.5)
                
                led1.set_rgb(0, 0, 0)
                
            """
        r = constrain(r, 0, 255)
        g = constrain(g, 0, 255)
        b = constrain(b, 0, 255)
        temp = _DataFormat(['B', 'B', 'B', 'B'])
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_LED_Color, r, g, b]))
        self._r = r
        self._g = g
        self._b = b

    # def set_brightness(self, brightness):
    #     """
    #         设置彩灯亮度

    #         Parameters
    #         ----------
    #         brightness : int
    #             设置LED彩灯的亮度，100为最亮，0为不发光

    #         Metas
    #         ---------------
    #         in :brightness
    #             range: 0~100

    #         Examples
    #         -------

    #         .. code-block:: python

    #             # 设置led大彩灯亮度为80
    #             led1.set_brightness(80)

    #         """
    #     if brightness > 100:
    #         return
    #     temp = _DataFormat(['B', 'B'])
    #     self._send_without_ack(
    #         _TYPE_REQUEST, temp.get_list([_CMD_LED_Brightness, brightness]))
    #     self.set_rgb(self._r, self._g, self._b)

    def fade_to_rgb(self, r, g, b, time, block=False, step=50):
        """
            控制彩灯由当前颜色在指定时间渐变到目标颜色

            Parameters
            ----------
            r : int
                目标红色：0~255
            g : int
                目标绿色：0~255
            b : int
                目标蓝色：0~255
            time : float
                渐变时间：0~60 s
                变化到目标颜色所用的时间
            block : bool
                阻塞参数：
                False: 不阻塞
                True: 阻塞
            step : int
                变化次数：
                在渐变时间内经过多少次变化达到目标颜色

            Metas
            ---------------
            in :r
                range: 0~255
            in :g
                range: 0~255
            in :b
                range: 0~255
            in :time
                range: 0~60
            in :block
                default: False
            in :step
                default: 50
                range: 1~100

            Examples
            -------

            .. code-block:: python

                # 设置彩灯在1秒内变换到淡红色(10，0，0)，再0.5秒内变到黄色（255，255，0）。最后关闭LED
                from wonderbits import Led
                led1 = Led()

                # 在1秒内变换到淡红色(10，0，0)，阻塞模式
                led1.fade_to_rgb(10, 0, 0, 1000, block=True)
                
                # 0.5秒内变到黄色（255，255，0），阻塞模式
                led1.fade_to_rgb(255, 255, 0, 500, block=True)

                # 最后关闭LED
                led1.set_rgb(0, 0, 0)

            """
        r = constrain(r, 0, 255)
        g = constrain(g, 0, 255)
        b = constrain(b, 0, 255)
        time_ms = int(time * 1000)
        time_ms = constrain(time_ms, 0, 65535)

        steptime_ms = time_ms // step
        steptime_ms = constrain(steptime_ms, 0, 65535)

        temp = _DataFormat(['B', 'B', 'B', 'B', 'list', 'list'])
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list([
                _CMD_LED_Fade, r, g, b,
                [steptime_ms // 256, steptime_ms % 256],
                [time_ms // 256, time_ms % 256]
            ]))
        if block:
            sleep(time)
