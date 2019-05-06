from reader import WatchProcess
from reader import CreonAPI


class WatchWithCreon(WatchProcess):
    def __init__(self):
        self.api = CreonAPI()
        self.chart = {}
        self.obj_watched = {}

    def watch(self, codes):
        for code in codes:
            if code in self.chart:
                print("Already in Watcher")
                continue

            self.chart[code] = []
            self.obj_watched[code] = self.api.watch_publisher
            self.obj_watched[code].subscribe(code, self)

    def stop_watch(self):
        for k, v in self.obj_watched.items():
            v.unsubscribe()

    def update_chart(self, item):
        code = item['code']
        time = item['time']
        cur = item['cur']
        self.make_min_chart(code, time, cur)

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
        minlen = len(self.chart[code])
        if (minlen > 0):
            # 현재 저장데이터는 오직 0 : 시간 1 : 시가 2: 고가 3: 저가 4: 종가
            if (self.chart[code][-1][0] == hhmm):
                item = self.chart[code][-1]
                bFind = True
                item[4] = cur
                if (item[2] < cur):
                    item[2] = cur
                if (item[3] > cur):
                    item[3] = cur

        if bFind == False:
            self.chart[code].append([hhmm, cur, cur, cur, cur])
