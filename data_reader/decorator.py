import time
import logging
from api import API


def limit_checker(original_function):
    '''
    시세조회 API call 제한관련 데커레이터

    :param original 함수
    :return wrapping 함수
    '''
    logger = logging.getLogger(__name__)
    api = API()

    def wrapper(*args, **kwargs):
        remain_time = api.get_limit_remain_time()
        remain_count = api.get_limit_remain_count('1')
        start = time.time()

        logger.info("REMAIN TIME: {0:.2f}s".format(remain_time / 1000))
        logger.info("REMAIN COUNT: {}".format(remain_count))

        if remain_count == 0:
            time.sleep((remain_time + 10) / 1000)

        delayed_time = time.time() - start
        logger.info("DELAYED: {0:.2f}s".format(delayed_time))

        return original_function(*args, **kwargs)

    return wrapper
