import time
from functools import wraps
import logging
import sys
import util
from logger import LoggerAdapter
from api import API
from query import Query


globals().update(Query.list())


def query_checker(original_function):
    """
    입력된 쿼리가 제대로 입력되었는지 검사하는 데커레이터

    :param original_function:
    :return:
    """
    logger = LoggerAdapter("QUERY CHECKER", logging.getLogger(__name__))
    api = API()

    def _field_key_check(chart_class, field_key):
        # 필드 키에 대한 예외처리 아직 안 끝났음
        if 6 in field_key and 37 not in field_key:
            logger.error("전일대비(6)키는 반드시 대비부호(37)키와 같이 사용되어야 함")
            sys.exit(1)

        if chart_class == DAY:
            if 10 in field_key or 11 in field_key:
                logger.warn("누적체결매도수량(10)과 누적체결매수수량(11)은 분,틱 요청일때만 제공")

        if chart_class == MIN:
            for key in field_key:
                if key in range(12, 22):
                    logger.warn("키(12~22)는 DAY CHART에만 들어옴")

        for key in field_key:
            if key in range(22, 27):
                logger.warn("키(22~26)은 들어오지 않음")

    def _code_check(stock_code):
        stock_list = api.get_stock_list('1')
        if stock_code not in stock_list:
            logger.error("STOCK CODE IS NOT IN KOSPI LIST")
            sys.exit(1)

    def _date_check(date_from, date_to):
        if date_to is None and date_from is None:
            logger.error("NO DATE PARAMETERS")
            sys.exit(1)

        today = util.get_today()
        date_to = util.str_to_date(date_to)
        date_from = util.str_to_date(date_from)

        if date_to > today and date_from > today:
            logger.error("INPUT DATE > TODAY")
            sys.exit(1)

        if date_to < date_from:
            logger.error("DATE_FROM > DATE_TO")
            sys.exit(1)

    def _get_value_from_kwargs(key, kwargs):
        if key in kwargs:
            return kwargs[key]
        else:
            return original_function.__kwdefaults__[key]

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        date_to = _get_value_from_kwargs('date_to', kwargs)
        date_from = _get_value_from_kwargs('date_from', kwargs)
        stock_code = _get_value_from_kwargs('code', kwargs)
        chart_class = _get_value_from_kwargs('chart_class', kwargs)
        field_key = _get_value_from_kwargs('field_key', kwargs)

        _date_check(date_from=date_from, date_to=date_to)
        _code_check(stock_code)
        _field_key_check(chart_class, field_key)

        return original_function(*args, **kwargs)

    return wrapper


def limit_checker(original_function):
    """
    시세조회 API call 제한관련 데커레이터

    :param original_function: 기존 함수
    :return: 래핑된 함수
    """
    logger = LoggerAdapter("LIMITATION CHECKER", logging.getLogger(__name__))
    api = API()

    @wraps(original_function)
    def wrapper(*args, **kwargs):
        remain_time = api.get_limit_remain_time()
        remain_count = api.get_limit_remain_count('1')
        start = time.time()

        logger.info("REMAIN TIME: {0:.2f}s".format(remain_time / 1000))
        logger.info("REMAIN COUNT: {}".format(remain_count))

        if remain_count == 0:
            time.sleep((remain_time + 100) / 1000)

        delayed_time = time.time() - start
        logger.info("DELAYED: {0:.2f}s".format(delayed_time))

        return original_function(*args, **kwargs)

    return wrapper
