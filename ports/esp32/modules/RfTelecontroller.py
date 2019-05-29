# RFTelecontroller.py
"""
射频遥控器模块/RfTelecontroller
===========================================
射频遥控器模块是具有通信功能的模块，可以进行一对多的传输，也可以接受其他射频模块发送的数据。

一般射频通信模块与射频遥控器一起使用。
射频遥控器上有9个不可编程的按键，无法获取按键状态，也无法使用按键事件。
按键功能为发送对应的键值，如：按下按键1，相当于发送数值1.

射频类型的模块要实现互相通讯需要通过编程设置为相同的通讯名称，才可互相通信。
但是由于某些特殊情况无法通过编程来统一通信名称，所以提供了一种射频通信模块和射频遥控器手动配对的方法。

射频通信模块和射频遥控器手动配对功能操作方法如下：
1. 长按射频通信模块上的按键指指示灯变为紫色（一般需要5秒钟）
2. 同时长按射频遥控器的按键1和按键9至蓝色指示灯闪烁
3. 在射频遥控器蓝灯闪烁结束前，射频通信模块指示灯恢复蓝色则表示配对成功

注意：
1. 射频通信模块指示灯变为紫色后可维持15秒配对状态，15秒后指示灯将恢复颜色
2. 若是射频遥控器蓝灯闪烁结束后，射频通信模块指示灯仍为紫色，则配对失败

"""

from public import DEVICE_TYPE, _TYPE_REQUEST, _CMD_Wireless_SetChannel, _CMD_Wireless_SetID, _CMD_Wireless_Send2, _CMD_Wirless_Mate
from ModuleObj import ModuleObj, constrain
from syspublic import Msg
from dataFormat import _DataFormat
import time
from EventManager import EventNameList, _return_event_start, _set_event_value, EventManager


class RfTelecontroller(ModuleObj):
    class _Event(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, RfTelecontroller, id, nameList)

        def msg_received(self, interval=50):
            """
                当收到新消息时会执行事件修饰的函数

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
            event = _return_event_start(0, EventManager._NUMBER_VALUE_TYPE,
                                        self.get_name('msg_received'))
            return event._compare(EventManager._UPDATE_ACTION, None, interval)

    class _Register(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, RfTelecontroller, id, nameList)

        def msg_received(self, interval=50):
            """
                注册接收消息事件，当收到消息的时候会触发事件并接收到数据，返回类型为float 

                Parameters
                ----------
                interval : int
                    表示每隔interval ms的时间检查值是否符合触发要求，如果符合会发送对应内容

                Metas
                ---------------
                in :interval
                    default: 50
                    range: 50~60000

                """
            register = _return_event_start(0, EventManager._NUMBER_VALUE_TYPE,
                                           self.get_name('msg_received'))
            register._register(EventManager._UPDATE_ACTION, None, interval)

    class _UnRegister(EventNameList):
        def __init__(self, id, nameList):
            EventNameList.__init__(self, RfTelecontroller, id, nameList)

        def msg_received(self):
            """
                注销接收消息事件

                """
            unregister = _return_event_start(0,
                                             EventManager._NUMBER_VALUE_TYPE,
                                             self.get_name('msg_received'))
            unregister._unregister()

    def __init__(self, id=1):
        ModuleObj.__init__(self, id - 1, DEVICE_TYPE['rfTelecontroller'])
        self._dataList = list()
        self._data_own = [0]
        self.lastValue = 0
        self.lastTime = 0

        self._name_list = list()
        self.event = RfTelecontroller._Event(id, self._name_list)
        self.register = RfTelecontroller._Register(id, self._name_list)
        self.unregister = RfTelecontroller._UnRegister(id, self._name_list)

    def _get_data(self, frame):
        
        
        if frame[3] == 1:
            temp = _DataFormat(['B'])
            value = temp.get_data_list(frame[4:])[0]
            if (time.ticks_ms() -
                    self.lastTime) > 300 or self.lastValue != value:
                self.lastValue = value
                self.lastTime = time.ticks_ms()
                if len(self._dataList) == 32:
                    self._dataList.pop(0)
                self._dataList.append(value)
                self._data_own[0] = value
                _set_event_value(self._name_list, self._data_own)
        elif frame[3] == 4:
            if len(self._dataList) == 32:
                self._dataList.pop(0)
            temp = _DataFormat(['f'])
            self._data_own[0] = round(temp.get_data_list(frame[4:])[0], 2)
            self._dataList.append(self._data_own[0])
            _set_event_value(self._name_list, self._data_own)

    def get_msg(self):
        """
            使用该函数可得到最近一次通信收到的内容，如果在程序开始后或使用clear_msg函数后没有发生过通信将返回None

            Returns
            -------
            float
                最新的通信内容，如果没有内容返回None

            Examples
            -------

            .. code-block:: python

                # 先将射频通信与射频遥控器配置成相同的名字
                rfCommunication1.init('public')
                rfTelecontroller1.init('public')
                
                # 使用射频通信模块发送1.23
                rfCommunication1.send(1.23)

                # 会在display1的第1行第1列显示1.23
                display1.print(1, 1, rfTelecontroller1.get_msg())

            """
        return self._data_own[0]

    def clear_msg(self):
        """
            清除最新的通信内容，在再次接收到新的通信内容之前调用get_msg只会返回None
            调用此函数并不会影响get_unread_msg_count和read的使用

            Examples
            -------

            .. code-block:: python

                # 清除最新的通信内容
                rfTelecontroller1.clear_msg()

            """
        self._data_own[0] = None

    def get_unread_msg_count(self):
        """
            该函数用于获取通信存储队列中未读内容的个数，最多存储32个未读内容

            Returns
            -------
            int
                通信存储队列中未读内容的个数，范围0~32

            Metas
            ---------------
            out :
                range: 0~32
                
            Examples
            -------

            .. code-block:: python

                # 当通信通信存储队列中有3个未读内容时，则会在display1的第1行第1列显示3
                display1.print(1, 1, rfTelecontroller1.get_unread_msg_count())
            
            """
        return len(self._dataList)

    def read(self):
        """
            该函数用于获取通信存储队列中未读内容，读取后会删除这个数据

            Returns
            -------
            float
                通信存储队列中最早的未读内容，如果没有未读的数据返回None


            Examples
            -------

            .. code-block:: python

                # 当通信通信存储队列中有未读内容时,，则会在display1的第1行第1列显示通信存储队列中最早的未读内容
                if rfCommunication1.get_unread_msg_count() > 0:
                    display1.print(1, 1, rfTelecontroller1.read())
            
            """
        if len(self._dataList) != 0:
            return self._dataList.pop(0)
        return None

    def _set_channel(self, Channel):
        temp = _DataFormat(['B', 'B'])
        self._send_without_ack(
            _TYPE_REQUEST, temp.get_list([_CMD_Wireless_SetChannel, Channel]))
        time.sleep_ms(100)

    def _set_id(self, ReceieveID):
        temp = _DataFormat(['B', 'B', 'B'])
        self._send_without_ack(
            _TYPE_REQUEST,
            temp.get_list(
                [_CMD_Wireless_SetID, ReceieveID // 256, ReceieveID % 256]))
        time.sleep_ms(100)

    def send(self, number):
        """
            发送数据。调用此函数后，与本模块通信名字相同的模块将会受到发送的内容
            
            Parameters
            ----------
            number : float
                发送的数值

            Metas
            ---------------
            in :number

            Examples
            -------

            .. code-block:: python

                # 发送数据
                rfTelecontroller1.send(1.23)

            """
        temp = _DataFormat(['B', 'B', 'f'])
        self._send_without_ack(_TYPE_REQUEST,
                               temp.get_list([_CMD_Wireless_Send2, 4, number]))

    def init(self, name='public'):
        """
            设置模块通信名字。只有通信名字相同的模块之间才可以互相通信，不想互相通信的模块需要设置不同的通信名字

            Parameters
            ----------
            name : str
                通信名字
            
            Metas
            ---------------
            in :name
                default: 'public'

            Examples
            -------

            .. code-block:: python

                # 设置模块通信名字
                rfTelecontroller1.init('Jack')

            """
        if name == None:
            temp = _DataFormat(['B'])
            self._send_without_ack(_TYPE_REQUEST,
                                   temp.get_list([_CMD_Wirless_Mate]))
        elif name == 'public':
            self._set_id(1)
            self._set_channel(1)
        else:
            seed = 131
            hashValue = 0
            for i in name:
                hashValue = hashValue * seed + ord(i)
            self._set_id(hashValue & 0xFFFF)
            self._set_channel((hashValue >> 16) % 84 + 1)
