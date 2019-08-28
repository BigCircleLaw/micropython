class Event(object):
    TRIGGER_FALSE_TO_TRUE = 0x00
    TRIGGER_TRUE_TO_FALSE = 0x01

    TRIGGER_CHANGED = 0x02
    TRIGGER_UPDATE = 0x03

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
