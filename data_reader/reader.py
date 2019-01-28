import sys
import pandas as pd
from creon import Creon


class Reader:
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
        self.creon = Creon()
        self.list_field_dict = {0: 'date', 1: 'time', 2: 'open', 3: 'high', 4: 'low', 5: 'close', 6: 'DoD', 8: 'volume',
                                9: 'trading_value', 10: 'sell_vol', 11: 'buy_vol', 12: 'the_number_of_shares',
                                13: 'market_cap', 14: 'frn_offer_limit_vol', 15:'frn_offer_avail_vol',
                                16: 'frn_ownership_vol', 17: 'foreigner_ownership_ratio', 18: 'adj_price_date',
                                19: 'adj_price_ratio', 20: 'int_net_buying', 21: 'int_cul_net_buying', 22: 'adl',
                                23: 'adr', 24: 'deposit', 25: 'turnover', 26: 'ratio_of_deals', 37: 'c_code'}

    def check_db_connection(self):
        '''
        DB 접속 여부를 확인하여 접속 여부를 화면에 출력하고 접속되지 않았다면 프로그램 종료
        :return: 접속여부에 대한 메시지 출력
        '''
        status, msg = self.creon.is_db_connect()
        print("Connection Status: {} {}".format(status, msg))
        if status != 0:
            return None

    def check_creon_connection(self):
        '''
        크레온 접속 여부를 확인하여, 접속 여부를 화면에 출력하고 접속되지 않았다면 프로그램 종료
        :return: 접속 여부에 대한 메시지 출력
        '''
        b_connected = self.creon.is_creon_connect()
        if b_connected == 0:
            print("Connection: Fail")
            sys.exit()
        else:
            print("Connection: Success")

    def get_stock_code_list(self, stock_market_num):
        '''
        미완성코드
        입력받은 마켓의 코드 리스트를 리턴
        :param stock_market_num:
            거래소: CPC_MARKET_KOSPI= 1,
            코스닥: CPC_MARKET_KOSDAQ= 2,
            K-OTC: CPC_MARKET_FREEBOARD= 3,
            KRX: CPC_MARKET_KRX= 4,
            KONEX: CPC_MARKET_KONEX= 5,
        :return: 코드 리스트
        '''
        self.check_connection()

        code_list = self.creon.get_stock_list(stock_market_num)
        for i, code in enumerate(code_list):
            secondCode = self.obj_CpCodeMgr.GetStockSectionKind(code)
            name = self.obj_CpCodeMgr.CodeToName(code)
            stdPrice = self.obj_CpCodeMgr.GetStockStdPrice(code)
            maxPrice = self.getMaxPrice(code)
            print(i, code, secondCode, stdPrice, maxPrice, name)

    def query_stock_chart(self, query):
        '''
        입력받은 쿼리에 대하여 차트 데이터 리턴
        :return: 입력한 주식 코드의 차트 데이터(pandas dataframe)
        '''

        self.check_creon_connection()
        self.creon.request_stock_chart(query)
        self.check_db_connection()

        list_field_name = [self.list_field_dict[key] for key in query[5]]
        dict_chart = {name: [] for name in list_field_name}
        receive_cnt = self.creon.get_chart_data_count()  # 수신개수

        for i in range(receive_cnt):
            dict_item = ({name: self.creon.get_data_value(pos, i) for pos, name in zip(range(len(list_field_name)), list_field_name)})
            for k, v in dict_item.items():
                dict_chart[k].append(v)

        print("CHART: {} {}".format(receive_cnt, dict_chart))
        return pd.DataFrame(dict_chart, columns=list_field_name)
