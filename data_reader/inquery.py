from enum import Enum


class Inquery(Enum):
    def __str__(self):
        return str(self.value)

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
