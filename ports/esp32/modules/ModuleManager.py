# ModuleManager.py
from syspublic import led, Msg
from public import _Addr_Master, _Addr_Broadcast, _Addr_Error, _TYPE_INIT, _CMD_ASK_UID, _TYPE_RESPONSE, RGB_B, RGB_LB, DEVICE_TYPE
from Sender import sender
from micropython import const
import time

# from machine import UART
# uart2 = UART(1, 125000)
# uart2.init(125000, bits=8, parity=None, stop=1, tx=10, rx=9)

_MODULE_ADDR_Start = const(0x10)


class ModuleManager:
    def __init__(self):
        self.definedModuleList = []
        # self.definedModuleTypeCount = {}
        self.moduleExistsList = []
        self.moduleExistsTypeCount = {}
        self.newModuleFlag = 0
        self.addrData = {}

    def start(self):
        del self.moduleExistsList[:]
        self.moduleExistsTypeCount.clear()
        self.sendACK(_Addr_Broadcast, _TYPE_INIT, [0, 0, 0, 0, _CMD_ASK_UID])
        i = 0
        while (i < 3) or self.newModuleFlag:
            self.newModuleFlag = 0
            i = i + 1
            led.Yellow()
            time.sleep_ms(50)
            led.black()
            time.sleep_ms(50)
        self.sort()
        self.loadId()
        led.Lblue()

    def put(self, uid):
        # print(len(uid))
        muid = [i for i in uid]
        # print(muid)
        self.moduleExistsList.append(muid)
        if uid[0] in self.moduleExistsTypeCount:
            self.moduleExistsTypeCount[uid[0]] += 1
        else:
            self.moduleExistsTypeCount[uid[0]] = 1
        self.newModuleFlag = 1

    def defineNewModule(self, newModule):
        self.definedModuleList.append(newModule)
        # if newModule.Type in self.definedModuleTypeCount:
        #     self.definedModuleTypeCount[newModule.Type] += 1
        # else:
        #     self.definedModuleTypeCount[newModule.Type] = 1

    def sort(self):
        # print(sorted(self.moduleExistsList))
        self.moduleExistsList.sort()
        # print(self.moduleExistsList)

    def loadId(self):
        self.addrData.clear()
        if len(self.moduleExistsList) == 0:
            return
        else:
            for i in range(len(self.moduleExistsList)):
                if self.moduleExistsList[i][0] in self.addrData.keys():
                    self.addrData[self.moduleExistsList[i][0]].append(
                        _MODULE_ADDR_Start + i)
                else:
                    self.addrData[self.moduleExistsList[i][0]] = [
                        _MODULE_ADDR_Start + i
                    ]
                # self.addrData.append(_MODULE_ADDR_Start + i)
                data = [0, 0, 0, 0, _MODULE_ADDR_Start + i, RGB_B
                        ] + self.moduleExistsList[i][1:]
                self.sendACK(_Addr_Broadcast, _TYPE_RESPONSE, data)
                time.sleep_ms(1)
        del data
        # self.setID()
        # self.sendID()

    def setID(self):
        for module in self.definedModuleList:
            module.setAddr()

    def getAddr(self, Id, Type):
        if Type in self.addrData.keys():
            return self.addrData[Type][Id]  # ['addr']
        # if (Type in self.moduleExistsTypeCount) and (Id < self.moduleExistsTypeCount[Type]):
        #     addrCount = 0
        #     for i in range(Type):
        #         if i in self.moduleExistsTypeCount:
        #             addrCount += self.moduleExistsTypeCount[i]
        #     # self.addrData[addrCount + Id - 1]['flag'] = 1
        #     return self.addrData[addrCount + Id] #['addr']
        return _Addr_Error

    def sendACK(self, addrValue, Type, data):
        # msg = Msg(addrValue, _Addr_Master, Type, len(data), data)
        data[0] = addrValue
        data[1] = _Addr_Master
        data[2] = Type
        data[3] = len(data) - 4
        sender.send(data)

    # def sendID(self):
    #     for i, uid in enumerate(self.moduleExistsList):
    #         data = [self.addrData[i], RGB_B] + uid[1:]
    #         # data = [self.addrData[i]['addr'],
    #         # RGB_B if self.addrData[i]['flag'] else RGB_LB]+uid[1:]
    #         self.sendACK(_Addr_Broadcast, _TYPE_RESPONSE, data)

    def doReport(self, id, data):
        for module in self.definedModuleList:
            if id == module.dstAddr:
                # uart2.write('s')
                module._get_data(data)
                # uart2.write('e')
                break

    def doUpdate(self):
        for module in self.definedModuleList:
            module._do_update_value()

    def getTypeAddrBuf(self):
        bufList = []
        bufList.append(len(self.moduleExistsTypeCount))
        # addrCount = 0
        for key in self.moduleExistsTypeCount:
            bufList.append(key)
            bufList.append(self.moduleExistsTypeCount[key])
            # for i in range(self.moduleExistsTypeCount[key]):
            #     bufList.append(self.addrData[addrCount])
            #     addrCount = addrCount + 1
        # for keyValue in range(len(DEVICE_TYPE)):
        #     if keyValue in self.moduleExistsTypeCount:
        #         bufList.append(keyValue)
        #         bufList.append(self.moduleExistsTypeCount[keyValue])
        #         for i in range(self.moduleExistsTypeCount[keyValue]):
        #             bufList.append(self.addrData[addrCount])
        #             # bufList.append(self.addrData[addrCount]['addr'])
        #             addrCount = addrCount + 1
        return bufList


moduleManager = ModuleManager()
