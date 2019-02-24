import sys
import pandas as pd
import logging
import datetime
from api import API
from decorator import limit_checker, query_checker
from query import Query
import util

globals().update(Query.list())


class Read:
    def __init__(self):
        '''
            0: 날짜(ulong)
            1:시간(long) - hhmm
            2:시가(long or float)
            3:고가(long or float)
            4:저가(long or float)
            5:종가(long or float)
            6:전일대비(long or float) - 주) 대비부호(37)과반드시같이요청해야함
            8:거래량(ulong or ulonglong)주) 정밀도만원단위
            9:거래대금(ulonglong)
            10:누적체결매도수량(ulong or ulonglong) -호가비교방식누적체결매도수량 (주) 10, 11 필드는분,틱요청일때만제공
            11:누적체결매수수량(ulong or ulonglong) -호가비교방식누적체결매수수량 (주) 10, 11 필드는분,틱요청일때만제공
            12:상장주식수(ulonglong)
            13:시가총액(ulonglong)
            14:외국인주문한도수량(ulong)
            15:외국인주문가능수량(ulong)
            16:외국인현보유수량(ulong)
            17:외국인현보유비율(float)
            18:수정주가일자(ulong) - YYYYMMDD
            19:수정주가비율(float)
            20:기관순매수(long)
            21:기관누적순매수(long)
            22:등락주선(long)
            23:등락비율(float)
            24:예탁금(ulonglong)
            25:주식회전율(float)
            26:거래성립률(float)
            37:대비부호(char) - 수신값은 GetHeaderValue 8 대비부호와동일
        '''
        self.logger = logging.getLogger( __name__)
        self.api = API()
        self.list_field_dict = {0: 'date', 1: 'time', 2: 'open', 3: 'high', 4: 'low', 5: 'close', 6: 'DoD', 8: 'volume',
                                9: 'trading_value', 10: 'sell_vol', 11: 'buy_vol', 12: 'the_number_of_shares',
                                13: 'market_cap', 14: 'frn_offer_limit_vol', 15:'frn_offer_avail_vol',
                                16: 'frn_ownership_vol', 17: 'foreigner_ownership_ratio', 18: 'adj_price_date',
                                19: 'adj_price_ratio', 20: 'int_net_buying', 21: 'int_cul_net_buying', 22: 'adl',
                                23: 'adr', 24: 'deposit', 25: 'turnover', 26: 'ratio_of_deals', 37: 'c_code'}

        self.full_time = util.get_open_time()

    def _check_db_connection(self):
        '''
        DB 접속 여부를 확인하여 접속 여부를 화면에 출력하고 접속되지 않았다면 프로그램 종료

        :return: 접속여부에 대한 메시지 출력
        '''
        status, msg = self.api.is_db_connect()
        if status != 0:
            self.logger.error("CONNECT TO DATABASE: Fail")
            return None
        self.logger.info("CONNECT TO DATABASE: Success")

    def _check_creon_connection(self):
        '''
        크레온 접속 여부를 확인하여, 접속 여부를 화면에 출력하고 접속되지 않았다면 프로그램 종료

        :return: 접속 여부에 대한 메시지 출력
        '''
        b_connected = self.api.is_creon_connect()
        if b_connected == 0:
            self.logger.error("CONNECT TO CREON SERVER: Fail")
            sys.exit()
        else:
            self.logger.info("CONNECT TO CREON SERVER: Success")

    def check_api_connection(self):
        '''
        종합적인 API connection을 체크

        :return: 접속 여부에 대한 메시지 출력
        '''
        self._check_creon_connection()
        self._check_db_connection()

    def get_name_from_code(self, code):
        return self.api.obj_CpCodeMgr.CodeToName(code)

    def get_stock_code_list(self, stock_market_num):
        '''
        입력받은 마켓의 코드 리스트를 리턴

        :param stock_market_num:
            거래소: CPC_MARKET_KOSPI= 1,
            코스닥: CPC_MARKET_KOSDAQ= 2,
            K-OTC: CPC_MARKET_FREEBOARD= 3,
            KRX: CPC_MARKET_KRX= 4,
            KONEX: CPC_MARKET_KONEX= 5,
        :return: 코드 리스트
        '''
        return self.api.get_stock_list(stock_market_num)

    @limit_checker
    def get_stock_chart(self, inquery):
        '''
        입력받은 쿼리에 대하여 차트 데이터 반환

        :param query: dictionary 형태의 Configuration
        :return: 입력한 주식 코드의 차트 데이터(pandas dataframe)
        '''
        self.api.request_stock_chart(inquery)
        list_field_name = [self.list_field_dict[key] for key in inquery[5]]
        dict_chart = {name: [] for name in list_field_name}
        receive_cnt = self.api.get_chart_data_count()

        for i in range(receive_cnt):
            dict_item = ({name: self.api.get_data_value(pos, i) for pos, name in zip(range(len(list_field_name)), list_field_name)})
            for k, v in dict_item.items():
                dict_chart[k].append(v)

        self.logger.debug("RECEIVE COUNT: {}".format(receive_cnt))
        return pd.DataFrame(dict_chart, columns=list_field_name)

    #def interpolator(self, chart):

    #def check_empty_in_min_chart(self, one_day_chart):
    #    difference_set = pd.concat(self.full_time, one_day_chart).drop_duplicates(keep=False)

    def split_by_day(self, chart, numdays=1):
        print(chart.iloc[0, 0])
        base = util.str_to_date(str(chart.iloc[0, 0]))
        date_list = [util.date_to_str(base + datetime.timedelta(days=x)) for x in range(0, numdays)]
        self.logger.debug("date_list: {}".format(date_list))
        split_chart = chart[chart['date'].isin(date_list)]
        print("XXXXXXXXXX\n", split_chart)
        return split_chart







    @query_checker
    def generate_query(self, *args,
                  code='A000030',
                  type=TERM,
                  date_to=util.date_to_str(util.get_today()),
                  date_from=util.date_to_str(util.get_today()),
                  req_cnt=20000,
                  field_key=[DATE, TIME, OPEN, HIGH],
                  chart_class=DAY,
                  gap_comp=NO,
                  adj_price=NO,
                  vol_class=INCLUDE_ALL):
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
