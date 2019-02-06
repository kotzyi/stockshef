import time
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
    '''
    obj_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')

    def wrapper(*args, **kwargs):
        remain_time = obj_CpCybos.LimitRequestRemainTime
        remain_count = obj_CpCybos.GetLimitRemainCount('1')
        start = time.time()

        print("REMAIN TIME: {0:.2f}s".format(remain_time / 1000))
        print("REMAIN COUNT: {}".format(remain_count))

        if remain_count == 0:
            time.sleep((remain_time + 10) / 1000)

        delayed_time = time.time() - start
        print("DELAYED: {0:.2f}s".format(delayed_time))

        return original_function(*args, **kwargs)

    return wrapper
