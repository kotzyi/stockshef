import time
import logging
import functools
import win32com.client
from PyQt5.QtWidgets import *


def data_checker(original_function):
    '''
    쿼리대로 데이터가 모두 들어왔는지 체크하는 데커레이터

    :param original_function: 데커레이터 받는 함수
    :return:
    '''

    def wrapper(*args, **kwargs):
        return original_function(*args, **kwargs)

    return wrapper


def limit_checker(original_function):
    '''
    시세조회 API call 제한관련 데커레이터

    :param original 함수
    :return wrapping 함수
    '''
    api = API()

    def wrapper(*args, **kwargs):
        remain_time = api.get_limit_remain_time()
        remain_count = api.get_limit_remain_count('1')
        start = time.time()

        logging.info("REMAIN TIME: {0:.2f}s".format(remain_time / 1000))
        logging.info("REMAIN COUNT: {}".format(remain_count))

        if remain_count == 0:
            time.sleep((remain_time + 10) / 1000)

        delayed_time = time.time() - start
        logging.info("DELAYED: {0:.2f}s".format(delayed_time))

        return original_function(*args, **kwargs)

    return wrapper


def exception(logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)

            # re-raise the exception
            raise

        return wrapper

    return decorator