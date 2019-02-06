from enum import Enum


class FieldKey(Enum):
    def __str__(self):
        return str(self.value)

    DATE = 0
    TIME = 1
    OPEN = 2
    HIGH = 3
    LOW = 4
    CLOSE = 5
    DAY_ON_DAY = 6
    VOL = 8
    TRADING_VALUE = 9
    SELLING_VOL = 10
    BUYING_VOL = 11
    NUM_SHARES = 12
    MKT_CAP = 13
    FOREIGN_OWNER_LIMIT = 14
    FOREIGN_OWNER_AVAIL = 15
    FOREIGN_OWNER_VOL = 16
    FOREIGN_OWNER_RATIO = 17
    ADJ_PRICE_DATE = 18
    ADJ_PRICE_RATIO = 19
    INT_NET_BUY = 20
    INT_CUM_NET_BUY = 21
    ADL = 22
    ADR = 23
    DEPOSIT = 24
    TURNOVER = 25
    RATIO_OF_DEALS = 26
    C_CODE = 37
