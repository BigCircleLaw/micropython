import time


class Event(object):
    TRIGGER_FALSE_TO_TRUE = 0x00
    TRIGGER_TRUE_TO_FALSE = 0x01

    TRIGGER_CHANGED = 0x02
    TRIGGER_UPDATE = 0x03

    register_dict = {}

    registerFlag = False

    def __init__(self,
                 source,
                 trigger_type,
                 value=None,
                 interval=None,
                 originalValueNum=None):
        self.source = source
        self.trigger_type = trigger_type
        self.value = value
        self.interval = interval
        self.originalValueNum = originalValueNum

    def __call__(self, func):
        self.source[0]._compare(func, self.source[1], self.source[2],
                                self.trigger_type, self.value, self.interval,
                                self.source[3])

    @classmethod
    def register_add(cls, index):
        cls.register_dict[index] = False
        cls.registerFlag = False

    @classmethod
    def get_register_state(cls, index=None):
        if index == None:
            return cls.registerFlag
        elif index in cls.register_dict:
            return (cls.register_dict[index] or cls.registerFlag)
        else:
            return True

    @classmethod
    def unregister(cls, index=None):
        if index is None:
            cls.registerFlag = True
            cls.register_dict.clear()
        elif index in cls.register_dict:
            cls.register_dict[index] = True
            time.sleep_ms(21)
            cls.register_dict.pop(index)

    @classmethod
    def get_register_list(cls):
        if len(cls.register_dict) > 0:
            key_list = cls.register_dict.keys()
            return ','.join(map(str, key_list))
        else:
            return ''
