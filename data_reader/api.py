import win32com.client


class API:
    def __init__(self):
        self.obj_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')
        self.obj_MarketWatch = win32com.client.Dispatch('CpSysDib.CpMarketWatchS')

    def request_stock_chart(self, request):
        '''
        데이터 차트 반환

        :param request: 아래 설명된 type 과 value로 이루어진 dictionary
        '''
        for key, value in request.items():
            self.obj_StockChart.SetInputValue(key, value)

        self.obj_StockChart.BlockRequest()

    def request_market_info(self, request):
        '''
        데이터 차트 반환

        :param request: 아래 설명된 type 과 value로 이루어진 dictionary
        '''
        for key, value in request.items():
            self.obj_MarketWatch.SetInputValue(key, value)

        self.obj_StockChart.BlockRequest()

    def is_db_connect(self):
        '''
        DB 접속정보의 상태와 메시지 반환

        :return: DB상태와 그에 따른 메시지
        '''
        status = self.obj_StockChart.GetDibStatus()
        msg = self.obj_StockChart.GetDibMsg1()
        return status, msg

    def is_creon_connect(self):
        '''
        creon plus에 접속하였는지 여부 반환

        :return: 접속 여부
            0: 실패
            1: 접속
        '''
        return self.obj_CpCybos.IsConnect

    def get_stock_capital(self, code):
        '''
        code에 해당하는 자본금규모구분 반환

        :pram code: 주식코드
        :return:자본금 규모 구분
            제외: CPC_CAPITAL_NULL  = 0,
            대: CPC_CAPITAL_LARGE  = 1,
            중: CPC_CAPITAL_MIDDLE  = 2,
            소: CPC_CAPITAL_SMALL  = 3
        '''
        return self.obj_CpCodeMgr.GetStockCapital(code)

    def get_stock_control_kind(self, code):
        '''
        감리코드 반환

        :param code: 주식 코드
        :return:
            정상: CPC_CONTROL_NONE   = 0,
            주의: CPC_CONTROL_ATTENTION= 1,
            경고: CPC_CONTROL_WARNING= 2,
            위험예고: CPC_CONTROL_DANGER_NOTICE= 3,
            위험: CPC_CONTROL_DANGER= 4,
        '''
        return self.obj_CpCodeMgr.GetStockControlKind(code)

    def get_stock_status_kind(self, code):
        '''
        주식코드에 대하여 현 상태 반환

        :param code: 주식코드
        :return:
            정상: CPC_STOCK_STATUS_NORMAL= 0,
            거래정지: CPC_STOCK_STATUS_STOP= 1,
            거래중단: CPC_STOCK_STATUS_BREAK= 2,
        '''
        return self.obj_CpCodeMgr.GetStockStatusKind(code)

    def get_stock_kospi_200_Kind(self, code):
        '''
        code 에해당하는KOSPI200 종목여부반환한다.

        :param code: 주식코드
        :return: KOSPI200 종목여부
            미채용: CPC_KOSPI200_NONE = 0,
            건설기계: CPC_KOSPI200_CONSTRUCTIONS_MACHINERY = 1,
            조선운송: CPC_KOSPI200_SHIPBUILDING_TRANSPORTATION = 2,
            철강소재: CPC_KOSPI200_STEELS_METERIALS = 3,
            에너지화학: CPC_KOSPI200_ENERGY_CHEMICALS = 4,
            정보통신: CPC_KOSPI200_IT = 5,
            금융: CPC_KOSPI200_FINANCE = 6,
            필수소비재: CPC_KOSPI200_CUSTOMER_STAPLES = 7,
            자유소비재: CPC_KOSPI200_CUSTOMER_DISCRETIONARY = 8,
        '''

    def get_stock_section_kind(self, code):
        '''
        주식 코드에 해당하는 부 구분코드를 반환

        :param code: 종목 코드
        :return: 부구분코드
            구분없음: CPC_KSE_SECTION_KIND_NULL= 0,
            주권: CPC_KSE_SECTION_KIND_ST   = 1,
            투자회사: CPC_KSE_SECTION_KIND_MF    = 2,
            부동산투자회사: CPC_KSE_SECTION_KIND_RT    = 3,
            선박투자회사: CPC_KSE_SECTION_KIND_SC    = 4,
            사회간접자본투융자회사: CPC_KSE_SECTION_KIND_IF = 5,
            주식예탁증서: CPC_KSE_SECTION_KIND_DR    = 6,
            신수인수권증권: CPC_KSE_SECTION_KIND_SW    = 7,
            신주인수권증서: CPC_KSE_SECTION_KIND_SR    = 8,
            주식워런트증권: CPC_KSE_SECTION_KIND_ELW = 9,
            상장지수펀드: CPC_KSE_SECTION_KIND_ETF = 10,
            수익증권: CPC_KSE_SECTION_KIND_BC    = 11,
            해외ETF: CPC_KSE_SECTION_KIND_FETF   = 12,
            외국주권: CPC_KSE_SECTION_KIND_FOREIGN = 13,
            선물: CPC_KSE_SECTION_KIND_FU    = 14,
            옵션: CPC_KSE_SECTION_KIND_OP    = 15,
        '''
        return self.obj_CpCodeMgr.GetStockSectionKind(code)

    def get_stock_par_price_chage_type(self, code):
        '''
        주식 코드에 해당하는 액면정보코드를 반환한다

        :param code: 주식코드
        :return: 액면정보코드
            해당없음: CPC_PARPRICE_CHANGE_NONE   = 0,
            액면분할: CPC_PARPRICE_CHANGE_DIVIDE   = 1,
            액면병합: CPC_PARPRICE_CHANGE_MERGE   = 2,
            기타: CPC_PARPRICE_CHANGE_ETC = 99,
        '''
        return self.obj_CpCodeMgr.GetStockParPriceChageType(code)

    def get_margin_rate(self, code):
        '''
        code에 해당하는 주식매수증거금율을 반환

        :param code: 주식코드
        :return: 주식매수증거금율
        '''
        return self.obj_CpCodeMgr.GetStockMarginRate(code)

    def get_max_price(self, code):
        '''
        code에 해당하는 상한가 반환

        :param code: 주식코드
        :return: 상한가
        '''
        return self.obj_CpCodeMgr.GetStockMaxPrice(code)

    def get_min_price(self, code):
        '''
        code에 해당하는 하한가 반환

        :param code: 주식코드
        :return: 하한가
        '''
        return self.obj_CpCodeMgr.GetStockMinPrice(code)

    def get_std_price(self, code):
        '''
        code에 해당하는 권리락 등으로 인한 기준가를 반환

        :param code: 주식코드
        :return: 기준가
        '''
        return self.obj_CpCodeMgr.GetStockStdPrice(code)

    def get_name(self, code):
        '''
        code에 해당하는 주식 명을 반환

        :param code: 주식코드
        :return: 주식명
        '''
        return self.obj_CpCodeMgr.CodeToName(code)

    def get_stock_list(self, stock_market_num):
        '''
        시장구분에따른 주식종목 배열을 반환

        :param stock_market_num: 마켓 번호
            구분없음: CPC_MARKET_NULL= 0,
            거래소: CPC_MARKET_KOSPI= 1,
            코스닥: CPC_MARKET_KOSDAQ= 2,
            K-OTC: CPC_MARKET_FREEBOARD= 3,
            KRX: CPC_MARKET_KRX= 4,
            KONEX: CPC_MARKET_KONEX= 5,
        :return: 입력한 시장구분(CPE_MARKET_KIND)에 해당하는 종목리스트(배열)
        '''
        return self.obj_CpCodeMgr.GetStockListByMarket(stock_market_num)

    def get_chart_header(self):
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

    def get_market_header(self):
        """

        :return:
        """
        header = {}
        for key in range(3):
            value = self.obj_MarketWatch.GetHeaderValue(key)
            header[key] = value
        return header

    def get_market_data_value(self, pos, i):
        return self.obj_MarketWatch.GetDataValue(pos, i)

    def get_chart_data_value(self, pos, i):
        '''
        원하는 데이터 필드 정보 반환 (현재는 사용되지 않음)

        :param pos:
        :param i:
        :return:
        '''
        return self.obj_StockChart.GetDataValue(pos, i)

    def get_limit_remain_time(self):
        '''
        요청에대한 남은 제한시간 반환

        :return: 남은 제한시간
        '''
        return self.obj_CpCybos.LimitRequestRemainTime

    def get_limit_remain_count(self, limit_type):
        '''
        남은 API 콜 수 반환

        :param limit_type: limitType: 요쳥에대한 제한 타입
            0: LT_TRADE_REQUEST - 주문관련 RQ 요청
            1: LT_NONTRADE_REQUEST - 시세관련 RQ 요청
            2: LT_SUBSCRIBE - 시세관련 SB
        :return: 제한을 하기전까지의 남은요청 개수
        '''
        return self.obj_CpCybos.GetLimitRemainCount(limit_type)