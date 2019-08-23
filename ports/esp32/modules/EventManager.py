import _thread
import time
from Event import Event


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
                # print(i, newValue[i], oldValue[i], newValue[i] != oldValue[i])
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

    def __init__(self, list_value, **feature):

        self.module_list_value = list_value
        self.data_update_list = [0 for i in range(len(list_value))]
        self.registerFlag = True

        # if 'numFlag' in feature:
        #     self.numFlag = feature['numFlag']
        # if 'varyValue' in feature:
        #     self.varyValue = feature['varyValue']

    def _triggerDecide(self,
                       valueType,
                       actionType,
                       compareValue,
                       position_of_list,
                       delta=None,
                       numFlag=None):
        if valueType == self._BOOL_VALUE_TYPE:
            if actionType == Event.TRIGGER_FALSE_TO_TRUE:
                return (
                    ((self.module_list_value[position_of_list] & numFlag) != 0
                     and (compareValue & numFlag) == 0),
                    self.module_list_value[position_of_list])
            elif actionType == Event.TRIGGER_TRUE_TO_FALSE:
                return (((self.module_list_value[position_of_list] &
                          self.numFlag) == 0
                         and (compareValue & numFlag) != 0),
                        self.module_list_value[position_of_list])
            elif actionType == Event.TRIGGER_CHANGED:
                return ((
                    (self.module_list_value[position_of_list] ^ compareValue)
                    & numFlag) != 0, self.module_list_value[position_of_list])
        elif valueType == self._NUMBER_VALUE_TYPE:
            if actionType == Event.TRIGGER_CHANGED:
                return _value_comparison(
                    self.module_list_value[position_of_list], compareValue,
                    delta if delta != None else 1)
            # elif actionType == Event.TRIGGER_UPDATE:
            #     if self.updateFlag:
            #         self.updateFlag = False
            #         return True, self.module_list_value[position_of_list]
            #     else:
            #         return False, self.module_list_value[position_of_list]
        elif valueType == self._STR_VALUE_TYPE:
            pass
        elif valueType == self._LIST_VALUE_TYPE:
            if actionType == Event.TRIGGER_CHANGED:
                return _value_comparison(
                    self.module_list_value[position_of_list], compareValue,
                    delta)
            # elif actionType == Event.TRIGGER_UPDATE:
            #     if self.updateFlag:
            #         self.updateFlag = False
            #         return True, self.module_list_value[position_of_list].copy()
            #     else:
            #         return False, self.module_list_value[position_of_list].copy()
        if actionType == Event.TRIGGER_UPDATE:
            if compareValue != self.data_update_list[position_of_list]:
                return True, self.data_update_list[position_of_list]
            else:
                return False, self.data_update_list[position_of_list]

    def _update_originalValue(self, position=None):
        update_list = self.data_update_list
        if position == None:
            for i in range(len(update_list)):
                update_list[i] += 1
        else:
            update_list[position] += 1

    def _register(self,
                  position_of_list,
                  valueType,
                  target,
                  actionType,
                  delta,
                  interval,
                  numFlag=None):
        if (valueType == self._BOOL_VALUE_TYPE and delta != None):
            print('Error: no have parameter.')
            return
        if interval == None:
            interval = 0.1

        if self._STR_VALUE_TYPE == valueType:
            send_str = '{\"type\":\"event\",\"target\":' + str(
                target) + ',\"valuetype\":\"string\",\"value\":\"'

        elif self._LIST_VALUE_TYPE == valueType:
            send_str = '{\"type\":\"event\",\"target\":' + str(
                target) + ',\"valuetype\":\"list\",\"value\":\"'
            # end_str = '\"}\n'
        else:
            send_str = '{\"type\":\"event\",\"target\":' + str(
                target) + ',\"value\":\"'
        end_str = '\"}'

        def event_task_run():
            delay = interval
            if Event.TRIGGER_UPDATE == actionType:
                ownData = self.data_update_list[position_of_list]
            elif self._LIST_VALUE_TYPE == valueType:
                ownData = self.module_list_value[position_of_list].copy()
            else:
                ownData = self.module_list_value[position_of_list]
            # print(id(ownData))
            # print(id(self.module_list_value[position_of_list]))
            while True:
                # print(self.eventList[1])
                bool_value, ownData = self._triggerDecide(
                    valueType, actionType, ownData, position_of_list, delta,
                    numFlag)
                # print(bool_value, ownData)
                if bool_value:
                    if valueType == self._BOOL_VALUE_TYPE:
                        print(
                            send_str + str(
                                (self.module_list_value[position_of_list] &
                                 numFlag) != 0) + end_str,
                            end='')
                    elif valueType == self._LIST_VALUE_TYPE:
                        print(
                            send_str + ','.join(
                                map(
                                    str,
                                    self.module_list_value[position_of_list].
                                    copy())) + end_str,
                            end='')

                    else:
                        print(
                            send_str + str(
                                self.module_list_value[position_of_list]) +
                            end_str,
                            end='')
                    time.sleep(delay)
                time.sleep_ms(10)
                # if self.registerFlag:
                #     _thread.exit()

        _thread.stack_size(_THREAD_STACK_SIZE)
        _thread.start_new_thread(event_task_run, ())

    def _unregister(self, actionType=None, delta=None):
        if self.registerFlag == False:
            self.registerFlag = True
        else:
            print('Error: this event isn\'t defined.')

    def _compare(self, actionType, delta, interval):
        if actionType == Event.TRIGGER_UPDATE:
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
        event_info[eventStr[0]] = EventManager(originalValueNum)
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
    def __init__(self, module, ID, name_list=None):
        # self.module = module
        # self.ID = ID
        self.name_dict = module.__module__[0].lower(
        ) + module.__module__[1:] + str(ID)
        self.event_name = name_list

    def get_name(self, valueName, name_list=None):
        name = self.name_dict + valueName
        temp = name_list if self.event_name == None else self.event_name
        if name not in temp:
            temp.append(name)

        return name, self.name_dict, valueName
