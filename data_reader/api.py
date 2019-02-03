import win32com.client


class API:
    def __init__(self):
        self.obj_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')

    def request_stock_chart(self, request):
        '''
        데이터 차트 반환
        :param request: 아래 설명된 type 과 value로 이루어진 dictionary
            0 - 종목코드(string): 주식(A003540), 업종(U001), ELW(J517016)의종목코드
            1 - 요청구분(char): '1' 기간으로 요청 '2' 개수로 요청
            2 - 요청종료일(ulong): YYYYMMDD형식으로데이터의마지막(가장최근) 날짜 Default(0) - 최근거래날짜
            3 - 요청시작일(ulong): YYYYMMDD형식으로데이터의시작(가장오래된) 날짜
            4 - 요청개수(ulong): 요청할데이터의개수
            5 - 필드(long or long array): 필드또는필드배열
                필드값
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
                    27:대비부호(char) - 수신값은 GetHeaderValue 8 대비부호와동일
            6 - 차트구분(char): # 'D':일, 'W':주, 'M':월, 'm':분, 'T':틱
            7 - 주기(ushort): Default-1
            8 - 갭보정여부(char): '0':갭 무보정(default) '1':갭보정
            9 - 수정주가(char): '0':무수정주가 '1':수정주가
            10 - 거래량구분(char): '1':시간외거래량모두포함[Default] '2': 장종료시간외거래량만포함 '3':시간외거래량모두제외 '4':장전시간외거래량만포함
        '''
        for key, value in request.items():
            self.obj_StockChart.SetInputValue(key, value)

        self.obj_StockChart.BlockRequest()

    def is_db_connect(self):
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

        :param code:
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
        code 에해당하는부구분코드를반환
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
        code 에해당하는액면정보코드를반환한다
        :param code:
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
        #
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
        code에 해당하는 주식명을 반환
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

    def get_chart_data_count(self):
        return self.obj_StockChart.GetHeaderValue(3)

    def get_data_value(self, pos, i):
        return self.obj_StockChart.GetDataValue(pos, i)

    def limit_request_remain_in_time(self):
        return self.obj_CpCybos.LimitRequestRemainTime

    def get_limit_remain_count(self, limit_type):
        '''

        :param limit_type: limitType: 요쳥에대한 제한 타입
            0: LT_TRADE_REQUEST - 주문관련 RQ 요청
            1: LT_NONTRADE_REQUEST - 시세관련 RQ 요청
            2: LT_SUBSCRIBE - 시세관련 SB
        :return: 제한을 하기전까지의 남은요청 개수
        '''
        return self.obj_CpCybos.GetLimitRemainCount(limit_type)