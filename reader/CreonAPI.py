import win32com.client
from reader import API
from reader import CreonWatchPublish


class CreonAPI(API):
    def __init__(self):
        self.obj_StockCur = win32com.client.Dispatch('DsCbo1.StockCur')
        self.obj_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')
        self.obj_MarketWatch = win32com.client.Dispatch('CpSysDib.CpMarketWatchS')
        self.watch_publisher = CreonWatchPublish()

    def login(self):
        """
        CreonAPI doesn't need login process

        :return: self.OK
        """
        return self.OK

    def connect(self):
        """
        CreonAPI doesn't need connect process.
        But, there is only check process to check db and creon reader connection.
        if db and creon connection is success, it returns self.OK. if not, it returns self.ERROR

        :return: self.OK or self.ERROR
        """
        if self.is_db_connect() and self.is_creon_connect():
            return self.OK
        else:
            return self.ERROR

    def get_stock_code_list(self, stock_market_number):
        """
        returns stock list

        :param stock_market_num: 마켓 번호
            거래소: CPC_MARKET_KOSPI= 1,
            코스닥: CPC_MARKET_KOSDAQ= 2,
        :return: 입력한 시장구분(CPE_MARKET_KIND)에 해당하는 딕셔너리
        """
        return {'kospi': self.obj_CpCodeMgr.GetStockListByMarket(1),
                'kosdaq': self.obj_CpCodeMgr.GetStockListByMarket(2)}

    def is_db_connect(self):
        '''
        DB 접속정보의 상태와 메시지 반환

        :return: DB상태와 그에 따른 메시지
        '''
        status = self.obj_StockChart.GetDibStatus()
        return status

    def is_creon_connect(self):
        '''
        creon plus에 접속하였는지 여부 반환

        :return: 접속 여부
            0: 실패
            1: 접속
        '''
        return self.obj_CpCybos.IsConnect

    def request_chart_data(self, request):
        '''
        데이터 차트 반환

        :param request: 아래 설명된 type 과 value로 이루어진 dictionary
        '''
        for key, value in request.items():
            self.obj_StockChart.SetInputValue(key, value)

        self.obj_StockChart.BlockRequest()

    def request_market_data(self, request):
        '''
        데이터 차트 반환

        :param request: 아래 설명된 type 과 value로 이루어진 dictionary
        '''
        for key, value in request.items():
            self.obj_MarketWatch.SetInputValue(key, value)

        self.obj_StockChart.BlockRequest()

    def get_chart_header_data(self):
        '''
        차트 데이터의 header 반환
        refer: https://documentation.help/CybosPlus/StockChart.htm

        :return: header의 정보 값
        '''
        header = {}
        for key in range(24):
            value = self.obj_StockChart.GetHeaderValue(key)
            header[key] = value
        return header

    def get_market_header_data(self):
        """

        :return:
        """
        header = {}
        for key in range(3):
            value = self.obj_MarketWatch.GetHeaderValue(key)
            header[key] = value
        return header

    def get_market_data(self, pos, i):
        return self.obj_MarketWatch.GetDataValue(pos, i)

    def get_chart_data(self, pos, i):
        '''
        원하는 데이터 필드 정보 반환 (현재는 사용되지 않음)

        :param pos:
        :param i:
        :return:
        '''
        return self.obj_StockChart.GetDataValue(pos, i)

    def check_limit_time(self):
        '''
        요청에대한 남은 제한시간 반환

        :return: 남은 제한시간
        '''
        return self.obj_CpCybos.LimitRequestRemainTime

    def check_limit_count(self, limit_type):
        '''
        남은 API 콜 수 반환

        :param limit_type: limitType: 요쳥에대한 제한 타입
            0: LT_TRADE_REQUEST - 주문관련 RQ 요청
            1: LT_NONTRADE_REQUEST - 시세관련 RQ 요청
            2: LT_SUBSCRIBE - 시세관련 SB
        :return: 제한을 하기전까지의 남은요청 개수
        '''
        return self.obj_CpCybos.GetLimitRemainCount(limit_type)
