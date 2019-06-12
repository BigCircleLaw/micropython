import _thread
import time


def _value_comparison(newValue, oldValue, varyValue):
    if type(newValue) != type(oldValue):
        return True, newValue
    elif isinstance(oldValue, list):
        # print(newValue)
        # print(oldValue)
        if len(newValue) != len(oldValue):
            return True, newValue.copy()
        else:
            for i in range(len(newValue)):
                if newValue[i] != oldValue[i]:
                    return True, newValue.copy()
            return False, oldValue
    else:
        return abs(newValue - oldValue) >= varyValue, oldValue if abs(
            newValue - oldValue) < varyValue else newValue


_THREAD_STACK_SIZE = 5632


class EventManager:

    _BOOL_VALUE_TYPE = 0x00
    _NUMBER_VALUE_TYPE = 0x01
    _STR_VALUE_TYPE = 0x02
    _LIST_VALUE_TYPE = 0x03

    _FALSE_TO_TRUE_ACTION = 0x00
    _TRUE_TO_FALSE_ACTION = 0x01

    _CHANGED_ACTION = 0x02
    _UPDATE_ACTION = 0x03

    # MORE_THAN_ACTION = 0x03
    # LESS_THAN_ACTION = 0x04

    def __init__(self, originalValueNum, valueType, eventList, **feature):
        self.originalValueNum = originalValueNum
        if valueType == EventManager._LIST_VALUE_TYPE:
            self.originalValue = list()
        else:
            self.originalValue = 0

        # self.recordValue = originalValue
        self.valueType = valueType
        self.registerFlag = True
        # self.actionType = actionType
        self.eventList = list()
        self.eventList.append(eventList[0])
        self.eventList.append(eventList[1])
        self.actionType = 0xFF
        if 'numFlag' in feature:
            self.numFlag = feature['numFlag']
        # if 'varyValue' in feature:
        #     self.varyValue = feature['varyValue']

    def _triggerDecide(self, actionType, compareValue, delta=None):
        if self.valueType == self._BOOL_VALUE_TYPE:
            if actionType == self._FALSE_TO_TRUE_ACTION:
                return (((self.originalValue & self.numFlag) != 0
                         and (compareValue & self.numFlag) == 0),
                        self.originalValue)
            elif actionType == self._TRUE_TO_FALSE_ACTION:
                return (((self.originalValue & self.numFlag) == 0
                         and (compareValue & self.numFlag) != 0),
                        self.originalValue)
            elif actionType == self._CHANGED_ACTION:
                return (((self.originalValue ^ compareValue) & self.numFlag) !=
                        0, self.originalValue)
        elif self.valueType == self._NUMBER_VALUE_TYPE:
            if actionType == self._CHANGED_ACTION:
                return _value_comparison(
                    self.originalValue, compareValue,
                    delta if delta != None else self.varyValue)
            elif actionType == self._UPDATE_ACTION:
                if self.updateFlag:
                    self.updateFlag = False
                    return True, self.originalValue
                else:
                    return False, self.originalValue
        elif self.valueType == self._STR_VALUE_TYPE:
            pass
        elif self.valueType == self._LIST_VALUE_TYPE:
            if actionType == self._CHANGED_ACTION:
                return _value_comparison(
                    self.originalValue, compareValue,
                    delta if delta != None else self.varyValue)
            elif actionType == self._UPDATE_ACTION:
                if self.updateFlag:
                    self.updateFlag = False
                    return True, self.originalValue
                else:
                    return False, self.originalValue

    # def _call_(self, func):
    #     def event_task_run():
    #         ownData = self.originalValue
    #         while True:
    #             bool_value, ownData = self._triggerDecide(ownData)
    #             if bool_value:
    #                 func()
    #             time.sleep_ms(50)
    #     _thread.stack_size(_THREAD_STACK_SIZE)
    #     _thread.start_new_thread(event_task_run, ())

    def _set_originalValue(self, value):
        self.originalValue = value[self.originalValueNum]
        if self.actionType == self._UPDATE_ACTION:
            self.updateFlag = True

    def _register(self, actionType, delta, interval):
        if (self.valueType == self._BOOL_VALUE_TYPE and delta != None):
            print('Error: no have parameter.')
            return
        if actionType == self._UPDATE_ACTION:
            self.actionType = actionType
            self.updateFlag = False
        # regStr = str(actionType) + '.' + str(delta)
        self.varyValue = delta
        self.interval = interval
        # if regStr not in self.registerFlag:
        #     self.registerFlag[regStr] = True
        if self.registerFlag:
            self.registerFlag = False

            if self._STR_VALUE_TYPE == self.valueType:
                send_str = '{\"type\":\"event\",\"module\":\"' \
                    + self.eventList[0] \
                    + '\",\"source\":\"' \
                    + self.eventList[1] \
                    + '\",\"valuetype\":\"string\",\"value\":\"'
                end_str = '\"}'
            elif self._LIST_VALUE_TYPE == self.valueType:
                send_str = '{\"type\":\"event\",\"module\":\"' \
                    + self.eventList[0] \
                    + '\",\"source\":\"' \
                    + self.eventList[1] \
                    + '\",\"valuetype\":\"list\",\"value\":\"'
                end_str = '\"}'
            else:
                send_str = '{\"type\":\"event\",\"module\":\"' \
                    + self.eventList[0] \
                    + '\",\"source\":\"' \
                    + self.eventList[1] \
                    + '\",\"value\":\"'
                end_str = '\"}'
            # if self.valueType == self._NUMBER_VALUE_TYPE:
            #     send_str = send_str + \
            #         str(delta if delta != None else self.varyValue)

            def event_task_run():
                ownData = self.originalValue
                while True:
                    # print(self.eventList[1])
                    bool_value, ownData = self._triggerDecide(
                        actionType, ownData, self.varyValue)
                    if bool_value:
                        if self.valueType == self._BOOL_VALUE_TYPE:
                            print(
                                send_str, ((ownData & self.numFlag) != 0),
                                end_str,
                                sep='')
                        if self.valueType == self._LIST_VALUE_TYPE:
                            print(
                                send_str,
                                ','.join(map(str, ownData)),
                                end_str,
                                sep='')

                        else:
                            print(send_str, ownData, end_str, sep='')
                    time.sleep_ms(self.interval)
                    if self.registerFlag:
                        # self.registerFlag = True
                        _thread.exit()

            _thread.stack_size(_THREAD_STACK_SIZE)
            _thread.start_new_thread(event_task_run, ())

    def _unregister(self, actionType=None, delta=None):
        # regStr = str(actionType) + '.' + str(delta)
        # if regStr in self.registerFlag:
        #     self.registerFlag[regStr] = True
        if self.registerFlag == False:
            self.registerFlag = True
        else:
            print('Error: this event isn\'t defined.')

    def _compare(self, actionType, delta, interval):
        if actionType == self._UPDATE_ACTION:
            self.actionType = actionType
            self.updateFlag = False

        def event_add_task(func):
            def event_task_run():
                ownData = self.originalValue
                while True:
                    bool_value, ownData = self._triggerDecide(
                        actionType, ownData, delta)
                    if bool_value:
                        func()
                    time.sleep_ms(interval)

            _thread.stack_size(_THREAD_STACK_SIZE)
            _thread.start_new_thread(event_task_run, ())

        return event_add_task


def event(tigger, interval=50):
    def event_add_task(func):
        def event_task_run():
            while True:
                if tigger():
                    func()
                time.sleep_ms(interval)

        _thread.stack_size(_THREAD_STACK_SIZE)
        _thread.start_new_thread(event_task_run, ())

    return event_add_task


event_info = dict()


def _return_event_start(originalValueNum, valueType, eventStr, **feature):
    if eventStr[0] not in event_info:
        event_info[eventStr[0]] = EventManager(originalValueNum, valueType,
                                               eventStr[1:3], **feature)
    return event_info[eventStr[0]]


def _set_event_value(eventNameList, valueList, select=None):
    if select == None:
        for name in eventNameList:
            if name in event_info:
                event_info[name]._set_originalValue(valueList)
    else:
        try:
            event_info[select]._set_originalValue(valueList)
        except:
            pass


class EventNameList:
    def __init__(self, module, id, nameList):
        # self.module = module
        # self.id = id
        self.name_dict = module.__module__[0].lower(
        ) + module.__module__[1:] + str(id)
        self.event_name = nameList

    def get_name(self, valueName):
        name = self.name_dict + valueName
        if name not in self.event_name:
            self.event_name.append(name)

        return name, self.name_dict, valueName
