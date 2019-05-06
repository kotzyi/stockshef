from reader import CreonEvent


class CreonWatchEvent(CreonEvent):
    def OnReceived(self):
        # 실시간 처리 - 현재가 주문 체결
        code = self.client.GetHeaderValue(0)  # 초
        name = self.client.GetHeaderValue(1)  # 초
        time = self.client.GetHeaderValue(18)  # 초
        exFlag = self.client.GetHeaderValue(19)  # 예상체결 플래그
        cprice = self.client.GetHeaderValue(13)  # 현재가
        diff = self.client.GetHeaderValue(2)  # 대비
        cVol = self.client.GetHeaderValue(17)  # 순간체결수량
        vol = self.client.GetHeaderValue(9)  # 거래량

        if exFlag != ord('2'):
            return

        item = {}
        item['code'] = code
        item['time'] = time
        item['diff'] = diff
        item['cur'] = cprice
        item['vol'] = vol

        # 현재가 업데이트
        self.caller.update_chart(item)
