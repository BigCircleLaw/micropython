import _thread
import time
from Event import Event
from wb import task_switch_then_back, send_a_data


def _value_comparison(new_value, old_value, vary_value):
    if type(new_value) != type(old_value):
        return True, new_value
    else:
        return abs(new_value - old_value) >= vary_value, old_value if abs(
            new_value - old_value) < vary_value else new_value


def _size_comparison(new_value, old_value):
    return (new_value > old_value) - (old_value > new_value)


def _str_trun_trigger(condition_str):
    # print(condition_str)
    def func(v):
        # print(v)
        return eval(condition_str, {'x': v})

    return func


_THREAD_STACK_SIZE = 5632


class EventManager:

    _BOOL_VALUE_TYPE = 0x00
    _NUMBER_VALUE_TYPE = 0x01
    _STR_VALUE_TYPE = 0x02
    _LIST_VALUE_TYPE = 0x03

    def __init__(self, list_value, **feature):

        self.module_list_value = list_value
        self.data_update_list = [0 for i in range(len(list_value))]

        # if 'numFlag' in feature:
        #     self.numFlag = feature['numFlag']
        # if 'vary_value' in feature:
        #     self.vary_value = feature['vary_value']

    def _triggerDecide(self,
                       valueType,
                       actionType,
                       compareValue,
                       position_of_list,
                       delta=None,
                       numFlag=None):
        if actionType == Event.TRIGGER_FALSE_TO_TRUE:
            if valueType == self._BOOL_VALUE_TYPE:
                return (
                    ((self.module_list_value[position_of_list] & numFlag) != 0
                     and (compareValue & numFlag) == 0),
                    self.module_list_value[position_of_list])
            else:
                a = bool(self.module_list_value[position_of_list])
                b = bool(compareValue)
                val = a == True and b == False
                if val:
                    if valueType == self._LIST_VALUE_TYPE:
                        return True, self.module_list_value[
                            position_of_list].copy()
                    return True, self.module_list_value[position_of_list]
                else:
                    return False, self.module_list_value[position_of_list]

        elif actionType == Event.TRIGGER_TRUE_TO_FALSE:
            if valueType == self._BOOL_VALUE_TYPE:
                return (((self.module_list_value[position_of_list] &
                          self.numFlag) == 0
                         and (compareValue & numFlag) != 0),
                        self.module_list_value[position_of_list])
            else:
                a = bool(self.module_list_value[position_of_list])
                b = bool(compareValue)
                val = a == False and b == True
                if val:
                    if valueType == self._LIST_VALUE_TYPE:
                        return True, self.module_list_value[
                            position_of_list].copy()
                    return True, self.module_list_value[position_of_list]
                else:
                    return False, self.module_list_value[position_of_list]
        elif actionType == Event.TRIGGER_CHANGED:
            if valueType == self._BOOL_VALUE_TYPE:
                return ((
                    (self.module_list_value[position_of_list] ^ compareValue)
                    & numFlag) != 0, self.module_list_value[position_of_list])
            elif valueType == self._LIST_VALUE_TYPE:
                val = _size_comparison(
                    self.module_list_value[position_of_list], compareValue)
                if val == 0:
                    return False, compareValue
                else:
                    return True, self.module_list_value[position_of_list].copy(
                    )
            else:
                return _value_comparison(
                    self.module_list_value[position_of_list], compareValue,
                    delta if delta is not None else 1)
        elif actionType == Event.TRIGGER_UPDATE:
            if compareValue != self.data_update_list[position_of_list]:
                return True, self.data_update_list[position_of_list]
            else:
                return False, self.data_update_list[position_of_list]
        else:
            # print(self.module_list_value[position_of_list])
            val = actionType(self.module_list_value[position_of_list])
            # print(val)
            if val:
                if valueType == self._LIST_VALUE_TYPE:
                    return True, self.module_list_value[position_of_list].copy(
                    )
                return True, self.module_list_value[position_of_list]
            else:
                return False, compareValue

    def _update_originalValue(self, position=None):
        update_list = self.data_update_list
        if position is None:
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
        Event.register_add(target)
        if (valueType == self._BOOL_VALUE_TYPE and delta != None):
            print('Error: no have parameter.')
            return
        if interval == None:
            interval = 0.1

        send_str = '{\"type\":\"event\",\"target\":' + str(
            target) + ',\"valuetype\":'

        if self._STR_VALUE_TYPE == valueType:
            send_str += '\"string\"'
        elif self._LIST_VALUE_TYPE == valueType:
            send_str += '\"list\"'
        elif self._NUMBER_VALUE_TYPE == valueType:
            send_str += '\"number\"'
        elif self._BOOL_VALUE_TYPE == valueType:
            send_str += '\"bool\"'

        send_str += ',\"value\":\"'
        end_str = '\"}'

        if type(actionType) is str:
            actionType = _str_trun_trigger(actionType)

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
                # send_a_data(target)
                bool_value, ownData = self._triggerDecide(
                    valueType, actionType, ownData, position_of_list, delta,
                    numFlag)
                # send_a_data(0xFF)
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
                task_switch_then_back()
                if Event.get_register_state(target):
                    _thread.exit()

        _thread.stack_size(_THREAD_STACK_SIZE)
        _thread.start_new_thread(event_task_run, ())

    def _compare(self,
                 func,
                 position_of_list,
                 valueType,
                 actionType,
                 delta,
                 interval,
                 numFlag=None):
        if interval is None:
            interval = 0.1

        if type(actionType) is str:
            actionType = _str_trun_trigger(actionType)

        def event_task_run():
            delay = interval
            if Event.TRIGGER_UPDATE == actionType:
                ownData = self.data_update_list[position_of_list]
            elif self._LIST_VALUE_TYPE == valueType:
                ownData = self.module_list_value[position_of_list].copy()
            else:
                ownData = self.module_list_value[position_of_list]

            try:
                while True:
                    bool_value, ownData = self._triggerDecide(
                        valueType, actionType, ownData, position_of_list,
                        delta, numFlag)
                    # print(bool_value, ownData)
                    if bool_value:
                        if self._LIST_VALUE_TYPE == valueType:
                            func(self.module_list_value[position_of_list].
                                 copy())
                        else:
                            func(self.module_list_value[position_of_list])
                        time.sleep(delay)
                    task_switch_then_back()
                    if Event.get_register_state():
                        _thread.exit()
            except KeyboardInterrupt:
                Event.unregister()
                _thread.exit()

        _thread.stack_size(_THREAD_STACK_SIZE)
        _thread.start_new_thread(event_task_run, ())
