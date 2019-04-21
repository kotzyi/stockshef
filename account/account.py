from api import API
import sys
import pandas as pd

class Account:

    def __init__(self):
        """
        0 - (string) 계좌번호
        1 - (string) 상품관리구분코드
        2 – (long) 요청건수[default:14] - 최대 50개
        """
        self.header = []
        self.data = []
        self.api = API()
        self.header_field_name = {0: '계좌명', 1: '결제 잔고수량', 2: '체결 잔고수량', 3: '평가금액', 4: '평가손익', 6: '대출금액', 7: '수신개수',
                                  8: '수익률', 9: 'D+2 예상 예수금', 10: '대주 평가금액', 11: '잔고평가금액', 12: '대주금액'}
        self.data_field_name = {0: '종목명', 1: '신용구분', 2: '대출일', 3:'결제 잔고수량', 4:'결제 장부단가', 5: '전일체결수량',
                                6: '금일체결수량', 7: '체결 잔고수량', 9: '평가금액', 10: '평가손익', 11: '수익률', 12: '종목코드',
                                13: '주문구분', 15: '매도가능수량', 16: '만기일', 17: '체결장부단가', 18: '손익단가'}
        self.account_numaber = self.api.obj_CpTrade.AccountNumber[0]  # 계좌번호
        self.account_flag = self.api.obj_CpTrade.GoodsList(self.account_number, 1)  # 주식상품 구분
        self.inquery = {0: self.account_number, 1: self.account_flag, 2: 50}

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

    def get_account(self):
        '''
        잔고정보 반환


        '''

        self.api.request_account_info(self.inquery)
        header = self.api.get_account_header()
        for key, value in header.item():
            self.header[self.header_field_name[key]] = value

        receive_cnt = header['수신개수']  # key=3 the number of rows
        account_dict = {name: [] for name in self.data_field_name}

        for i in range(receive_cnt):
            dict_item = ({name: self.api.get_account_data_value(pos, i) for pos, name in zip(range(len(self.data_field_name)), self.data_field_name)})
            for k, v in dict_item.items():
                account_dict[k].append(v)

        self.logger.debug("RECEIVE COUNT: {}".format(receive_cnt))
        return header, pd.DataFrame(account_dict, columns=self.data_field_name)
