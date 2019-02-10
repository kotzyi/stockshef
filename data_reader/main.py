import os
import logging.config
import yaml
import config
import datetime
import util
from read import Read
from fieldkey import FieldKey
from inquery import Inquery


globals().update(Inquery.list())
globals().update(FieldKey.list())

def main():
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
    read = Read()
    read.check_api_connection()

    stock_code = 'A005930'
    #date_from = '20190102' #마지막 날짜
    chart = get_min_chart(code=stock_code, date_from='20181207', date_to='20181218')


    filepath = os.path.join(config.BASE_DIR,
                 'data/chart/{}.csv'.format(stock_code))
    #chart.to_csv(filepath, mode='w')
    #print(chart)

def store_chart(chart, code):
    filepath = os.path.join(config.BASE_DIR, 'data/chart/{}.csv'.format(code))
    util.create_file(filepath)
    chart.to_csv(filepath, mode='a')
    ("Store Success")


def get_day_chart(code, date_to, date_from):
    '''
    얻을 수 있는 모든 정보를 포함한 Day-Chart 반환

    :param code: 주식 코드
    :param date_to: 얻고자 하는 최종 날짜
    :param date_from: 시작 날짜
    :return: 주식 코드에 대한 일-차트 가능한 모든 데이터
    '''
    read = Read()

    field_key = [DATE, OPEN, HIGH, LOW, CLOSE, VOL, TRADING_VALUE, NUM_SHARES, MKT_CAP, FOREIGN_OWNER_LIMIT,
                 FOREIGN_OWNER_AVAIL, FOREIGN_OWNER_VOL, FOREIGN_OWNER_RATIO, ADJ_PRICE_DATE, ADJ_PRICE_RATIO,
                 INT_NET_BUY, INT_CUM_NET_BUY, C_CODE]

    inquery = read.gen_inquery(code=code, date_from=date_from, date_to=date_to, field_key=field_key)
    chart = read.get_stock_chart(inquery)
    return chart


def get_min_chart(code, date_to, date_from):
    '''
    얻을 수 있는 모든 정보를 포함한 Minute-Chart 반환

    :param code: 주식 코드
    :param date_to: 최종 날짜
    :param date_from: 시작 날짜
    :return: 주식 코드에 대한 분-차트 가능한 모든 데이터
    '''
    logger = logging.getLogger(__name__)
    logger.info("START TO READ MINUTE CHART DATA")
    read = Read()
    field_key = [DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL, TRADING_VALUE, SELLING_VOL, BUYING_VOL, C_CODE]
    last_date = None
    last_time = None
    chart = None
    # 분 차트에서 2017-01-18이 마지막 날

    while not (last_date == date_from and last_time == "901"):
        inquery = read.gen_inquery(code=code, date_from=date_from, date_to=date_to, field_key=field_key, chart_class=MIN)
        chart = read.get_stock_chart(inquery)
        if chart is None:
            logger.error("CHART: EMPTY")
            return None

        last_date = str(chart.iloc[-1, 0])
        last_time = str(chart.iloc[-1, 1])
        store_chart(chart.head(1524), code)  # 1524개가 분 차트에서 4일치 데이터
        new_date_to = datetime.datetime.strptime(last_date, "%Y%m%d").strftime('%Y%m%d')
        logger.debug("NEW_DATE_TO: {}".format(new_date_to))
        logger.debug("DATE_TO: {}".format(date_to))

        if new_date_to == date_to:
            break
        date_to = new_date_to

        logger.debug("CHART:\n{}".format(chart))
        logger.debug("LAST: {}-{} TO: {}".format(last_date, last_time, date_from))

    logger.info("DATA READING: SUCCESS {}~{}".format(last_date, date_to))
    return chart


def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    '''
    로깅 설정

    :param default_path:
    :param default_level:
    :param env_key:
    :return:
    '''
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), value)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == '__main__':
    setup_logging()
    main()
