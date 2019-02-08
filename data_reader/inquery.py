from aenum import IntEnum, NoAlias


class Inquery(IntEnum, settings=NoAlias):
    def __get__(self, instance, owner):
        return self.value

    @staticmethod
    def list():
        return [(e.name, e.value) for e in Inquery]

    TERM = 49
    COUNT = 50
    NO = 49
    YES = 50
    TICK = ord('T')
    MIN = ord('m')
    DAY = ord('D')
    WEEK = ord('W')
    MONTH = ord('M')
    INCLUDE_ALL = 1
    INCLUDE_ONLY_AFTER_HOURS = 2
    INCLUDE_ON_TIME = 3
    INCLUDE_PRE_MARKET = 4
