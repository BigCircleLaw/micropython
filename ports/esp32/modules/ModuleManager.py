# ModuleManager.py
from wb import led
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
        self.moduleExistsTypeCount = {}
        self.newModuleFlag = 0
        self.addrData = {}

    def defineNewModule(self, newModule):
        self.definedModuleList.append(newModule)

    def findModuleList(self, ID, type):
        for module in self.definedModuleList:
            if (ID == module.id) and (type == module._type):
                return True, module
        return False, None

    def doReport(self, ID, data):
        for module in self.definedModuleList:
            if ID == module.dstAddr:
                module._get_data(data)
                break

    def doUpdate(self):
        for module in self.definedModuleList:
            module._do_update_value()


moduleManager = ModuleManager()
