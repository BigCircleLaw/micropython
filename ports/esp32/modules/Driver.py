# Driver.py
"""
驱动模块/Driver
=============================
此模块可连接两个直流电机两个舵机，分别是：

直流电机A
直流电机B
舵机1
舵机2

"""

from public import DEVICE_TYPE
from wb import _TYPE_REQUEST
from ModuleObj import ModuleObj
from wb import constrain

from wb import _DataFormat
from utime import sleep

_CMD_DC_STOP = 0x08  # 停止直流电机工作
_CMD_DC_SET = 0x09  # 设置直流电机的方向和速度
_CMD_DC_Servo = 0x0A  # 设置舵机角度
_CMD_Servo_OFF = 0x0B  # 关闭舵机

# STOP 3


class Driver(ModuleObj):
    _DC_A = 1
    _DC_B = 2
    _FWD = 1
    _REV = 2

    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['driver'])

    def set_motor_a(self, speed, time=0.01, block=False):
        """
            设置电机A转动

            Parameters
            ----------
            speed : int
                转速：-100~100
                符号表示转动方向，绝对值为转动速度
            time : float
                变速时间，从当前转速转变到设置转速用到的时间，单位 s
                默认值为0.01 
            block : bool
                阻塞参数：
                False：不阻塞
                True：阻塞

            Metas
            ---------------
            in :speed
                range: -100~100
            in :time
                default:0.01
                range: 0.01~60
            in :block
                default: False

            Examples
            -------

            .. code-block:: python

                # 控制电机转动
                from wonderbits import Driver
                import time

                driver1 = Driver()
                while True:
                    # 先让a b 电机都以50的功率正转, 且舵机1，2都转到30度
                    driver1.set_motor_a(50)
                    driver1.set_motor_b(50)
                    driver1.set_servo1(30)
                    driver1.set_servo2(30)
                    time.sleep(3) # 持续3秒

                    # 让a b 电机都以50的功率反转, 且舵机1，2都转到90度
                    driver1.set_motor_a(-50)
                    driver1.set_motor_b(-50)
                    driver1.set_servo1(90)
                    driver1.set_servo2(90)
                    time.sleep(3) # 持续3秒

                    # 停止所有电机
                    driver1.stop_motor_a()
                    driver1.stop_motor_b()
                    driver1.stop_servo1()
                    driver1.stop_servo2()

                    time.sleep(5) # 持续5秒
            """
        temp = _DataFormat('BBBBH')
        if speed < 0:
            dir = Driver._REV
        else:
            dir = Driver._FWD
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list(
                [_CMD_DC_SET, Driver._DC_A, dir, speed,
                 int(time * 1000)]))
        if block:
            sleep(time)

    def stop_motor_a(self):
        """
            电机A停止转动

            Examples
            -------
            未提供。可参考 `set_motor_a`_ 的使用案例

            """
        # temp = _DataFormat('BB')
        # self._send_without_ack(_TYPE_REQUEST,
        #                        temp.get_list([_CMD_DC_STOP, Driver._DC_A]))
        self.set_motor_a(0)

    def set_motor_b(self, speed, time=0.01, block=False):
        """
            设置电机B转动

            Parameters
            ----------
            speed : int
                转速：-100~100
                符号表示转动方向，绝对值为转动速度
            time : float
                变速时间，从当前转速转变到设置转速用到的时间，单位 s
                默认值为10 
            block : bool
                阻塞参数：
                False: 不阻塞
                True: 阻塞

            Metas
            ---------------
            in :speed
                range: -100~100
            in :time
                default:0.01
                range: 0.01~60
            in :block
                default: False

            Examples
            -------
            未提供。可参考 `set_motor_a`_ 的使用案例

            """
        if speed < 0:
            dir = Driver._FWD
        else:
            dir = Driver._REV
        temp = _DataFormat('BBBBH')
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list(
                [_CMD_DC_SET, Driver._DC_B, dir, speed,
                 int(time * 1000)]))
        if block:
            sleep(time)

    def stop_motor_b(self):
        """
            电机B停止转动

            Examples
            -------
            未提供。可参考 `set_motor_a`_ 的使用案例

            """
        # temp = _DataFormat('BB')
        # self._send_without_ack(_TYPE_REQUEST,
        #                        temp.get_list([_CMD_DC_STOP, Driver._DC_B]))
        self.set_motor_b(0)

    def set_servo1(self, angle):
        """
            设置舵机1转动到指定角度
            使用此函数后舵机1将拥有维持角度的扭矩，施加外力改变舵机1的角度会很困难

            Parameters
            ----------
            angle : int
                角度：0~180

            Metas
            ---------------
            in :angle
                range: 0~180

            Examples
            -------
            未提供。可参考 `set_motor_a`_ 的使用案例

            """
        angle = constrain(angle, 0, 180)
        temp = _DataFormat('BHB')
        self._send_without_ack(
            _TYPE_REQUEST, temp.get_list([_CMD_DC_Servo,
                                          int(angle * 100), 2]))

    def stop_servo1(self):
        """
            关闭舵机1
            使用此函数后舵机1将失去维持角度的扭矩，施加外力可以轻松改变舵机1的角度

            Examples
            -------
            未提供。可参考 `set_motor_a`_ 的使用案例

            """
        temp = _DataFormat('BB')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_Servo_OFF, 2]))

    def set_servo2(self, angle):
        """
            设置舵机2转动到指定角度
            使用此函数后舵机2将拥有维持角度的扭矩，施加外力改变舵机2的角度会很困难

            Parameters
            ----------
            angle : int
                角度：0~180

            Metas
            ---------------
            in :angle
                range: 0~180

            Examples
            -------
            未提供。可参考 `set_motor_a`_ 的使用案例

            """
        angle = constrain(angle, 0, 180)
        temp = _DataFormat('BHB')
        self._send_without_ack(
            _TYPE_REQUEST, temp.get_list([_CMD_DC_Servo,
                                          int(angle * 100), 1]))

    def stop_servo2(self):
        """
            关闭舵机2
            使用此函数后舵机2将失去维持角度的扭矩，施加外力可以轻松改变舵机2的角度

            Examples
            -------
            未提供。可参考 `set_motor_a`_ 的使用案例

            """
        temp = _DataFormat('BB')
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_Servo_OFF, 1]))
