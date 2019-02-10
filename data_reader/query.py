from aenum import IntEnum, NoAlias
import logging


class Query(IntEnum, settings=NoAlias):
    '''
    query 형식은 아래와 같음
    query = { 0: code, 1: req_code, 2: date_to, 3: date_from, 5: list_field_key, 6: chart_class, 8: gap_comp, 9: adj_price, 10: vol_class }

    :param code:  종목코드(string): 주식(A003540), 업종(U001), ELW(J517016)의 종목코드 *앞의 A를 반드시 포함하는 코드
    :param req_code: 요청구분(char): ord('1') 기간으로 요청 ord('2') 개수로 요청
    :param date_to: 요청종료일(ulong): YYYYMMDD 형식으로 데이터의 마지막(가장 최근) 날짜 Default(0) - 최근거래날짜
    :param date_from: 요청시작일(ulong): YYYYMMDD 형식으로 데이터의 시작(가장 오래된) 날짜
    :param req_cnt: 요청개수(ulong): 요청할데이터의개수
    :param list_field_key: 필드(long or long array): 필드 또는 필드배열
        0: 날짜(ulong)
        1:시간(long) - hhmm
        2:시가(long or float)
        3:고가(long or float)
        4:저가(long or float)
        5:종가(long or float)
        6:전일대비(long or float) - 주) 대비부호(37)과반드시같이요청해야함 X
        8:거래량(ulong or ulonglong) - 주) 정밀도만원단위
        9:거래대금(ulonglong)
        10:누적체결매도수량(ulong or ulonglong) -호가비교방식누적체결매도수량 (주) 10, 11 필드는분,틱요청일때만제공
        11:누적체결매수수량(ulong or ulonglong) -호가비교방식누적체결매수수량 (주) 10, 11 필드는분,틱요청일때만제공
        12:상장주식수(ulonglong) (DAY만 들어옴)
        13:시가총액(ulonglong) (DAY만 들어옴)
        14:외국인주문한도수량(ulong) (DAY만 들어옴)
        15:외국인주문가능수량(ulong) (DAY만 들어옴)
        16:외국인현보유수량(ulong) (DAY만 들어옴)
        17:외국인현보유비율(float) (DAY만 들어옴)
        18:수정주가일자(ulong) - YYYYMMDD (DAY만 들어옴)
        19:수정주가비율(float) (DAY만 들어옴)
        20:기관순매수(long) (DAY만 들어옴)
        21:기관누적순매수(long) (DAY만 들어옴)
        22:등락주선(long) X
        23:등락비율(float) X
        24:예탁금(ulonglong) X
        25:주식회전율(float) X
        26:거래성립률(float) X
        37:대비부호(char) - 수신값은 GetHeaderValue 8 대비부호와동일
    :param chart_class: 차트구분(char): # ord('D'):일,ord('W'):주,ord('M'):월,ord('m'):분,ord('T'):틱
    :param gap_comp: 갭보정여부(char): '0':갭 무보정(default) '1':갭보정
    :param adj_price: 수정주가(char): '0':무수정주가 '1':수정주가
    :param vol_class: 거래량구분(char): '1':시간외 거래량 모두 포함[Default] '2': 장 종료시간외 거래량만 포함 '3':시간외 거래량 모두 제외 '4':장전시간외 거래량만 포함
    '''
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def __get__(self, instance, owner):
        return self.value

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

    @staticmethod
    def list():
        return [(e.name, e.value) for e in Query]

    def gen_inquery(self,
                  code='A000030',
                  type=self.TERM,
                  date_to=datetime.datetime.today().strftime('%Y%m%d'),
                  date_from=datetime.datetime.today().strftime('%Y%m%d'),
                  req_cnt=20000,
                  field_key=[self.DATE, self.TIME, self.OPEN, self.HIGH],
                  chart_class=self.DAY,
                  gap_comp=self.NO,
                  adj_price=self.NO,
                  vol_class=self.INCLUDE_ALL):
        """
        차트 데이터를 조회할 수 있는 Dict 형태의 Query 를 반환

        :param code:  종목코드(string): 주식(A003540), 업종(U001), ELW(J517016)의 종목코드 *앞의 A를 반드시 포함하는 코드
        :param req_code: 요청구분(char): ord('1') 기간으로 요청 ord('2') 개수로 요청
        :param date_to: 요청종료일(ulong): YYYYMMDD 형식으로 데이터의 마지막(가장 최근) 날짜 Default(0) - 최근거래날짜
        :param date_from: 요청시작일(ulong): YYYYMMDD 형식으로 데이터의 시작(가장 오래된) 날짜
        :param req_cnt: 요청개수(ulong): 요청할데이터의개수
        :param list_field_key: 필드(long or long array): 필드 또는 필드배열
        :param chart_class: 차트구분(char): # ord('D'):일,ord('W'):주,ord('M'):월,ord('m'):분,ord('T'):틱
        :param gap_comp: 갭보정여부(char): '0':갭 무보정(default) '1':갭보정
        :param adj_price: 수정주가(char): '0':무수정주가 '1':수정주가
        :param vol_class: 거래량구분(char): '1':시간외 거래량 모두 포함[Default] '2': 장 종료시간외 거래량만 포함 '3':시간외 거래량 모두 제외 '4':장전시간외 거래량만 포함
        :return: 입력한 파라메터 형태의 차트 데이터
        """
        query = {0: code, 1: type, 2: date_to, 3: date_from, 4: req_cnt, 5: field_key, 6: chart_class, 8: gap_comp,
         9: adj_price, 10: vol_class}
        self.logger.debug("GENERATED QUERY: {}".format(query))

        return query
