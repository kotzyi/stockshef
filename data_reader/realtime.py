import sys
from PyQt5.QtWidgets import *
import win32com.client
import ctypes
from api import API
from read import Read
import logging
import os
import yaml
import logging.config
from collect import Collect
import threading


class CpEvent:
    def set_params(self, client, name, caller):
        self.client = client  # CP 실시간 통신 object
        self.name = name  # 서비스가 다른 이벤트를 구분하기 위한 이름
        self.caller = caller  # callback 을 위해 보관

    def OnReceived(self):
        # 실시간 처리 - 현재가 주문 체결
        if self.name == 'stockcur':
            code = self.client.GetHeaderValue(0)  # 초
            name = self.client.GetHeaderValue(1)  # 초
            timess = self.client.GetHeaderValue(18)  # 초
            exFlag = self.client.GetHeaderValue(19)  # 예상체결 플래그
            cprice = self.client.GetHeaderValue(13)  # 현재가
            diff = self.client.GetHeaderValue(2)  # 대비
            cVol = self.client.GetHeaderValue(17)  # 순간체결수량
            vol = self.client.GetHeaderValue(9)  # 거래량

            if exFlag != ord('2'):
                return

            item = {}
            item['code'] = code
            item['time'] = timess
            item['diff'] = diff
            item['cur'] = cprice
            item['vol'] = vol

            # 현재가 업데이트
            self.caller.updateCurData(item)

            return


class CpPublish:
    def __init__(self, name, serviceID):
        self.name = name
        self.obj = win32com.client.Dispatch(serviceID)
        self.bIsSB = False

    def Subscribe(self, var, caller):
        if self.bIsSB:
            self.Unsubscribe()

        if (len(var) > 0):
            self.obj.SetInputValue(0, var)

        handler = win32com.client.WithEvents(self.obj, CpEvent)
        handler.set_params(self.obj, self.name, caller)
        self.obj.Subscribe()
        self.bIsSB = True

    def Unsubscribe(self):
        if self.bIsSB:
            self.obj.Unsubscribe()
        self.bIsSB = False


class CpPBStockCur(CpPublish):
    def __init__(self):
        super().__init__('stockcur', 'DsCbo1.StockCur')


class MinChart:
    def __init__(self):
        self.api = API()
        self.collect = Collect()
        self.min_data = {}
        self.obj_cur = {}
        self.list_field_name = ['time', 'open', 'high', 'low', 'close']
        self.logger = logging.getLogger(__name__)

    def stop(self):
        for k, v in self.obj_cur.items():
            v.Unsubscribe()

    def add_code(self, code):
        if (code in self.min_data):
            return

        self.min_data[code] = []
        self.obj_cur[code] = CpPBStockCur()
        self.obj_cur[code].Subscribe(code, self)

    def update_cur_data(self, item):
        code = item['code']
        time = item['time']
        cur = item['cur']
        self.make_minc_hart(code, time, cur)

    def make_min_chart(self, code, time, cur):
        hh, mm = divmod(time, 10000)
        mm, tt = divmod(mm, 100)
        mm += 1
        if (mm == 60):
            hh += 1
            mm = 0

        hhmm = hh * 100 + mm
        if hhmm > 1530:
            hhmm = 1530
        bFind = False
        minlen = len(self.min_data[code])
        if (minlen > 0):
            # 현재 저장데이터는 오직 0 : 시간 1 : 시가 2: 고가 3: 저가 4: 종가
            if (self.min_data[code][-1][0] == hhmm):
                item = self.min_data[code][-1]
                bFind = True
                item[4] = cur
                if (item[2] < cur):
                    item[2] = cur
                if (item[3] > cur):
                    item[3] = cur

        if bFind == False:
            self.min_data[code].append([hhmm, cur, cur, cur, cur])

        return

    def save(self, code):
        self.logger.info('Save Minute Data: {} - {}'.format(code, self.api.obj_CpCodeMgr.CodeToName(code)))
        self.min_data[code].append(["231", "22", "111", "23", "cur"]) #!!!!테스트용 인풋 실제 구현에서는 추후 지워야 함
        for item in self.min_data[code]:
            self.collect.save_realtime(code, item)


def save_chart(code_list, min_data, sec=60.0):
    for i in range(len(code_list)):
        min_data.save(code_list[i])

    threading.Timer(sec, save_chart, [code_list, min_data, sec]).start()


def main():
    read = Read()
    logger = logging.getLogger(__name__)

    read.check_api_connection()
    min_data = MinChart()
    code_list = read.get_stock_code_list('1')
    code_list = code_list[:10]

    for i, code in enumerate(code_list): #최대 구독 가능 개수 < 400
        logger.info("code: {}  name:{}".format(code, read.get_name_from_code(code)))
        min_data.add_code(code)

    save_chart(code_list, min_data)


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


if __name__ == "__main__":
    setup_logging()
    load_configuration()
    main()

