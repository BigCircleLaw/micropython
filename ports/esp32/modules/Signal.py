# Signal.py
"""
信号模块/Signal
=============================
此模块内置1个LED灯、1个蜂鸣器和1个振动马达。
可编程控制灯的颜色，蜂鸣器响声频率，和震动强度。

"""
from public import DEVICE_TYPE
from wb import _TYPE_REQUEST
from ModuleObj import ModuleObj
from wb import constrain

from wb import _DataFormat
from utime import sleep

_CMD_LED_RGB = 0x08  # LED模拟输出颜色
_CMD_BUZZER_OFF = 0x09
_CMD_BUZZER_FRE = 0x0A  # 设置无源蜂鸣器频率
_CMD_VIBRATIONMOTOR_SET = 0x0B  # 设置振动马达震动强度
_CMD_BUZZER_SET = 0x0C  # 设置无源蜂鸣器频率，占空比
_CMD_SignalRGB_Fade = 0x0D  # 设置RGB渐变
_CMD_PlayANode = 0x0E  # 播放一个声音


class Signal(ModuleObj):
    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['signal'])

    def set_rgb(self, r, g, b):
        """
            设置LED灯颜色（r,g,b 参数都设置为0时，关闭LED）

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

                # 控制LED灯颜色变换
                from wonderbits import Signal
                import time
                signal1 = Signal()

                # LED灯在按红-绿-蓝色变化，每次持续一秒
                signal1.set_rgb(20, 0, 0)
                time.sleep(1)
                signal1.set_rgb(0, 20, 0)
                time.sleep(1)
                signal1.set_rgb(0, 0, 20)
                time.sleep(1)
                signal1.set_rgb(0, 0, 0) # 关闭LED灯

            """
        r = constrain(r, 0, 255)
        g = constrain(g, 0, 255)
        b = constrain(b, 0, 255)
        temp = _DataFormat('BBBB')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_LED_RGB, b, g, r]))

    def set_buzzer(self, frequency):
        """
            设置蜂鸣器声音频率（Hz）
            设置频率为0表示关闭蜂鸣器

            Parameters
            ----------
            frequency : int
                频率：0~20000 Hz

            Metas
            ---------------
            in :frequency
                range: 0~20000

            Examples
            -------

            .. code-block:: python
                
                # 设置蜂鸣器音调越来越高
                from wonderbits import Signal
                signal1 = Signal()

                for f in range(20000):
                    signal1.set_buzzer(f)

            """
        if frequency == 0:
            cmd = _CMD_BUZZER_OFF
        else:
            cmd = _CMD_BUZZER_FRE
        temp = _DataFormat('BH')
        self._send_without_ack(_TYPE_REQUEST, temp.get_list([cmd, frequency]))

# {
#     struct BuzzerContent buf = {_CMD_BUZZER_SET, Fre, duty}
#     this->_send_without_ack(_TYPE_REQUEST, (unsigned char * )&buf, sizeof(struct BuzzerContent))
# }

    def set_vibration(self, strength):
        """
            设置震动马达的震动幅度
            值越大表示震动幅度越大，设置为0时停止震动

            Parameters
            ----------
            strength : int
                振动幅度：0~100

            Metas
            ---------------
            in :strength
                range: 0~100

            Examples
            -------

            .. code-block:: python

                # 感受震动马达在不同强度震动的差别
                from wonderbits import Signal
                import time
                signal1 = Signal() 

                while True:
                    signal1.set_vibration(20)
                    time.sleep(2)

                    signal1.set_vibration(50)
                    time.sleep(2)

                    signal1.set_vibration(100)
                    time.sleep(2)

            """
        temp = _DataFormat('BB')
        self._send_without_ack(
            _TYPE_REQUEST, temp.get_list([_CMD_VIBRATIONMOTOR_SET, strength]))

    def play_a_note(self, frequency, time, block=False):
        """
            控制蜂鸣器发出一个音调，并持续一段时间

            Parameters
            ----------
            frequency : int
                频率：20~20000 Hz
            time : float
                时间: 0.05~60 s
            block : bool
                阻塞参数：
                False: 不阻塞
                True: 阻塞

            Metas
            ---------------
            in :frequency
                range: 20~20000
            in :time
                range: 0.05~60
            in :block
                default: False

            Examples
            -------

            .. code-block:: python

                # 演奏一首小星星，我不会.... 那就音调越来越高吧
                from wonderbits import Signal
                signal1 = Signal() 

                signal1.play_a_note(800, 0.5)
                signal1.play_a_note(900, 0.5)
                signal1.play_a_note(1000, 0.5)
                signal1.play_a_note(1100, 0.5)
                signal1.play_a_note(1200, 0.5)
                signal1.play_a_note(1300, 0.5)
                
                signal1.play_a_note(0, 0.5)

            """
        temp = _DataFormat('BHH')
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list([_CMD_PlayANode, frequency,
                           int(time * 1000)]))
        if block:
            sleep(time)


# define aaaa 10
# void Signal:: setRGB(unsigned char color)
# {
#     if (color == RGB_B)
#     {
#         this->setRGB(0, 0, aaaa)
#     }
#     if (color == RGB_G)
#     {
#         this->setRGB(0, aaaa, 0)
#     }
#     if (color == RGB_R)
#     {
#         this->setRGB(aaaa, 0, 0)
#     }
#     if (color == RGB_OFF)
#     {
#         this->setRGB(0, 0, 0)
#     }
#     if (color == RGB_OFF)
#     {
#         this->setRGB(0, 0, 0)
#     }
#     if (color == RGB_Y)
#     {
#         this->setRGB(aaaa, aaaa, 0)
#     }
#     if (color == RGB_P)
#     {
#         this->setRGB(aaaa, 0, aaaa)
#     }
#     if (color == RGB_W)
#     {
#         this->setRGB(aaaa, aaaa, aaaa)
#     }
#     if (color == RGB_LB)
#     {
#         this->setRGB(0, aaaa, aaaa)
#     }
# }
