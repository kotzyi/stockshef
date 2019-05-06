from reader import CollectProcess
from reader import CreonAPI
import pandas as pd
import sys
import datetime


class CollectWithCreon(CollectProcess):
    def __init__(self):
        self.api = CreonAPI
        self.TERM = 49
        self.COUNT = 50
        self.NO = 49
        self.YES = 50
        self.TICK = ord('T')
        self.MIN = ord('m')
        self.DAY = ord('D')
        self.WEEK = ord('W')
        self.MONTH = ord('M')
        self.INCLUDE_ALL = 1
        self.INCLUDE_ONLY_AFTER_HOURS = 2
        self.INCLUDE_ON_TIME = 3
        self.INCLUDE_PRE_MARKET = 4

        self.DATE = 0
        self.TIME = 1
        self.OPEN = 2
        self.HIGH = 3
        self.LOW = 4
        self.CLOSE = 5
        self.DAY_ON_DAY = 6
        self.VOL = 8
        self.TRADING_VALUE = 9
        self.SELLING_VOL = 10
        self.BUYING_VOL = 11
        self.NUM_SHARES = 12
        self.MKT_CAP = 13
        self.FOREIGN_OWNER_LIMIT = 14
        self.FOREIGN_OWNER_AVAIL = 15
        self.FOREIGN_OWNER_VOL = 16
        self.FOREIGN_OWNER_RATIO = 17
        self.ADJ_PRICE_DATE = 18
        self.ADJ_PRICE_RATIO = 19
        self.INT_NET_BUY = 20
        self.INT_CUM_NET_BUY = 21
        self.ADL = 22
        self.ADR = 23
        self.DEPOSIT = 24
        self.TURNOVER = 25
        self.RATIO_OF_DEALS = 26
        self.C_CODE = 37
        self.list_field_dict = {0: 'date', 1: 'time', 2: 'open', 3: 'high', 4: 'low', 5: 'close', 6: 'DoD', 8: 'volume',
                                9: 'trading_value', 10: 'sell_vol', 11: 'buy_vol', 12: 'the_number_of_shares',
                                13: 'market_cap', 14: 'frn_offer_limit_vol', 15: 'frn_offer_avail_vol',
                                16: 'frn_ownership_vol', 17: 'foreigner_ownership_ratio', 18: 'adj_price_date',
                                19: 'adj_price_ratio', 20: 'int_net_buying', 21: 'int_cul_net_buying', 22: 'adl',
                                23: 'adr', 24: 'deposit', 25: 'turnover', 26: 'ratio_of_deals', 37: 'c_code'}

        self.list_header_dict = {0: '종목코드', 1: '필드개수', 2: '필드배열', 3: '수신개수', 4: '마지막봉틱수',
                                 5: '최근거래일', 6: '전일종가', 7: '현재가', 8: '대비부호', 9: '대비', 10: '거래량',
                                 11: '매도호가', 12: '매수호가', 13: '시가', 14: '고가', 15: '저가', 16: '거래대금',
                                 17: '종목상태', 18: '상장주식수', 19: '자본금', 20: '전일거래량', 21: '최근갱신시간',
                                 22: '상한가', 23: '하한가'}

        self.list_market_dict = {0: '시간', 1: '작업구분', 2: '특이사항 코드'}
        self.date_from = '2010-01-02'

    def collect(self, chart_class):
        dataframes = {}
        code_lists = self.api.get_stock_code_list()

        for key, codes in code_lists.items():
            for code in codes:
                if chart_class == self.DAY:
                    dataframes[code] = self.collect_day_chart_data(code)
                elif chart_class == self.MIN:
                    dataframes[code] = self.collect_min_chart_data(code)
                else:
                    print("ERROR")
                    sys.exit(1)

        return dataframes

    def collect_min_chart_data(self, code):
        last_date = None
        last_time = None
        chart = None
        # 분 차트에서 2017-01-18이 마지막 날

        while not (last_date == self.date_from and last_time == "901"):
            query = self.generate_stock_chart_query(code=code, chart_class=self.MIN)
            new_chart = self.get_chart_data_by_query(query)
            if new_chart is None:
                print("CHART: NO RETURN DATA")
                return None

            new_chart = self.split_by_day(new_chart, num_day=4)
            interpolated_chart = self.interpolator(new_chart, num_day=4)

            last_date = str(interpolated_chart["date"].iloc[-1])
            last_time = str(interpolated_chart["time"].iloc[-1])

            chart = self.append_dataframe(chart, interpolated_chart)
            new_date_to = (datetime.datetime.strptime(last_date, '%Y%m%d') - datetime.timedelta(1)).strftime('%Y%m%d')

            if new_date_to == date_to:
                break

            date_to = new_date_to

        return chart

    def collect_day_chart_data(self, code):
        query = self.generate_stock_chart_query(code=code, chart_class=self.DAY)
        chart = self.get_chart_data_by_query(query)
        return chart

    def get_chart_data_by_query(self, query):
        """
        입력받은 쿼리에 대하여 차트 데이터 반환

        :param query: dictionary 형태의 Configuration
        :return: 입력한 주식 코드의 차트 데이터(pandas dataframe)
        """
        self.api.request_chart_data(query)
        list_field_name = [self.list_field_dict[key] for key in query[5]]
        dict_chart = {name: [] for name in list_field_name}
        header = self.api.get_chart_header()
        receive_cnt = header[3] # key=3 the number of rows

        for i in range(receive_cnt):
            dict_item = ({name: self.api.get_chart_data(pos, i) for pos, name in zip(range(len(list_field_name)), list_field_name)})
            for k, v in dict_item.items():
                dict_chart[k].append(v)

        return pd.DataFrame(dict_chart, columns=list_field_name)

    def generate_stock_chart_query(self, *args, code='A000030', chart_class=None):
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

        if chart_class == self.DAY:
            field_key = [self.DATE, self.OPEN, self.HIGH, self.LOW, self.CLOSE, self.VOL, self.TRADING_VALUE,
                         self.NUM_SHARES, self.MKT_CAP, self.FOREIGN_OWNER_LIMIT, self.FOREIGN_OWNER_AVAIL,
                         self.FOREIGN_OWNER_VOL, self.FOREIGN_OWNER_RATIO, self.ADJ_PRICE_DATE, self.ADJ_PRICE_RATIO,
                         self.INT_NET_BUY, self.INT_CUM_NET_BUY, self.C_CODE]
        elif chart_class == self.MIN:
            field_key = [self.DATE, self.TIME, self.OPEN, self.HIGH, self.LOW, self.CLOSE, self.VOL, self.TRADING_VALUE,
                         self.SELLING_VOL, self.BUYING_VOL, self.C_CODE]
        else:
            print("ERROR!!")
            sys.exit()

        query = {0: code, 1: self.TERM, 2: datetime.datetime.today().strftime('%Y%m%d'), 3: self.date_from, 4: 20000,
                 5: field_key, 6: chart_class, 8: self.NO, 9: self.NO, 10: self.INCLUDE_ALL}

        return query

    def interpolator(self, chart, num_day=4):
        """
        거래가 일어나지 않아 중간에 비어있는 데이터를 interpolation 하기 위한 함수
        :param chart:
        :return:
        """
        new_chart = pd.DataFrame()
        full_time = None
        for i in range(num_day):
            full_time = self.append_dataframe(full_time, self.full_time)
        full_time = reversed(full_time.values.tolist())

        #Add empty rows
        for chart_index, row in chart.iterrows():
            for time_index, time in enumerate(full_time):
                if int(time[0]) == row["time"]:
                    new_chart = new_chart.append(row)
                    break

                new_row = pd.Series([str(row["date"]), str(time[0])], index=['date', 'time'])
                #new_row = pd.Series([row["date"], time[0], null], index=row.index.tolist())
                new_chart = new_chart.append(new_row, ignore_index=True)

        new_chart = new_chart.interpolate(method='linear', limit_direction='forward', axis=0)
        new_chart['date'] = new_chart['date'].astype(int).astype('str')
        new_chart['time'] = new_chart['time'].astype(int).astype('str')
        return new_chart

    def split_by_day(self, chart, num_day=1):
        """
        차트에서 원하는 날짜의 데이터(가장 최근의 날부터 - numdays 만큼) 스플릿해서 차트를 반환하는 함수
        :param chart: 주식 차트 데이터
        :param numdays: 원하는 날짜의 수
        :return:
        """
        all_date_list = chart["date"].drop_duplicates().tolist()
        date_list = all_date_list[:num_day]
        split_chart = chart[chart['date'].isin(date_list)]
        return split_chart

    def append_dataframe(self, chart, new_chart):
        if chart is None:
            return new_chart

        return chart.append(new_chart)
