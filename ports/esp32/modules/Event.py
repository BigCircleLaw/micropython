class Event(object):
    TRIGGER_FALSE_TO_TRUE = 0x00
    TRIGGER_TRUE_TO_FALSE = 0x01

    TRIGGER_CHANGED = 0x02
    TRIGGER_UPDATE = 0x03

    TRIGGER_MORE = 0x04
    TRIGGER_LESS = 0x05

    def __init__(self):
        pass

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
