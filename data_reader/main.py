import os
import logging.config
import yaml
import datetime
import util
from collect import Collect
from read import Read
from query import Query


globals().update(Query.list())


def main():
    read = Read()
    collect = Collect()
    read.check_api_connection()
    stock_code = 'A000020'

    #code_list = read.get_stock_code_list('1')
    chart = get_min_chart(code=stock_code, date_from='20180305', date_to='20180308')
    collect.save_chart(chart, stock_code)  # 1524개가 분 차트에서 4일치 데이터
    #for code in code_list:
    #    chart = get_min_chart(code=code, date_from='20130102', date_to=util.date_to_str(util.get_today()))
    #    collect.save_chart(chart, code)  # 1524개가 분 차트에서 4일치 데이터


def get_day_chart(code, date_to, date_from):
    '''
    얻을 수 있는 모든 정보를 포함한 Day-Chart 반환

    :param code: 주식 코드
    :param date_to: 얻고자 하는 최종 날짜
    :param date_from: 시작 날짜
    :return: 주식 코드에 대한 일-차트 가능한 모든 데이터
    '''
    logger = logging.getLogger(__name__)
    logger.info("START TO READ DAY CHART")
    read = Read()

    field_key = [DATE, OPEN, HIGH, LOW, CLOSE, VOL, TRADING_VALUE, NUM_SHARES, MKT_CAP, FOREIGN_OWNER_LIMIT,
                 FOREIGN_OWNER_AVAIL, FOREIGN_OWNER_VOL, FOREIGN_OWNER_RATIO, ADJ_PRICE_DATE, ADJ_PRICE_RATIO,
                 INT_NET_BUY, INT_CUM_NET_BUY, C_CODE]

    inquery = read.generate_query(code=code, date_from=date_from, date_to=date_to, field_key=field_key)
    chart = read.get_stock_chart(inquery)
    logger.info("DATA READING: Success ({} ~ {})".format(date_from, date_to))

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
    logger.info("START TO READ MINUTE CHART")
    read = Read()
    collect = Collect()
    field_key = [DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL, TRADING_VALUE, SELLING_VOL, BUYING_VOL, C_CODE]
    last_date = None
    last_time = None
    chart = None
    # 분 차트에서 2017-01-18이 마지막 날

    while not (last_date == date_from and last_time == "901"):
        inquery = read.generate_query(code=code, date_from=date_from, date_to=date_to, field_key=field_key, chart_class=MIN)
        new_chart = read.get_stock_chart(inquery)
        if new_chart is None:
            logger.error("CHART: NO RETURN DATA")
            return None

        new_chart = read.split_by_day(new_chart, num_day=4)
        interpolated_chart = read.interpolator(new_chart, num_day=4)

        last_date = str(interpolated_chart["date"].iloc[-1])
        last_time = str(interpolated_chart["time"].iloc[-1])

        chart = collect.append_dataframe(chart, interpolated_chart)
        new_date_to = util.date_to_str(util.str_to_date(last_date) - datetime.timedelta(1))

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
