import os
import logging.config
import yaml
import datetime
import util
from read import Read
from query import Query


globals().update(Query.list())


def main():
    read = Read()
    read.check_api_connection()

    stock_code = 'A005930'
    chart = get_day_chart(code=stock_code, date_from='20181207', date_to='20181218')
    print(chart)

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
    chart = None

    field_key = [DATE, OPEN, HIGH, LOW, CLOSE, VOL, TRADING_VALUE, NUM_SHARES, MKT_CAP, FOREIGN_OWNER_LIMIT,
                 FOREIGN_OWNER_AVAIL, FOREIGN_OWNER_VOL, FOREIGN_OWNER_RATIO, ADJ_PRICE_DATE, ADJ_PRICE_RATIO,
                 INT_NET_BUY, INT_CUM_NET_BUY, C_CODE]

    inquery = gen_inquery(code=code, date_from=date_from, date_to=date_to, field_key=field_key)
    #chart = read.get_stock_chart(inquery)
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
        inquery = gen_inquery(code=code, date_from=date_from, date_to=date_to, field_key=field_key, chart_class=MIN)
        chart = read.get_stock_chart(inquery)
        if chart is None:
            logger.error("CHART: EMPTY")
            return None

        last_date = str(chart.iloc[-1, 0])
        last_time = str(chart.iloc[-1, 1])
        store_chart(chart.head(1524), code)  # 1524개가 분 차트에서 4일치 데이터
        new_date_to = datetime.datetime.strptime(last_date, "%Y%m%d").strftime('%Y%m%d')

        logger.debug("CHART:\n{}".format(chart))
        logger.debug("LAST: {}-{} TO: {}".format(last_date, last_time, date_from))

        if new_date_to == date_to:
            break

        date_to = new_date_to

    logger.info("DATA READING: Success ({} ~ {})".format(last_date, date_to))
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


def load_configuration(default_path='setting.yaml', env_key='MAIN_CFG'):
    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), value)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())



if __name__ == '__main__':
    setup_logging()
    load_configuration()
    main()
