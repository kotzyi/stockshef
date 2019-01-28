from reader import Reader


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
    :param chart_class: 차트구분(char): # ord('D'):일,ord('W'):주,ord('M'):월,ord('m'):분,ord('T'):틱
    :param gap_comp: 갭보정여부(char): '0':갭 무보정(default) '1':갭보정
    :param adj_price: 수정주가(char): '0':무수정주가 '1':수정주가
    :param vol_class: 거래량구분(char): '1':시간외 거래량 모두 포함[Default] '2': 장 종료시간외 거래량만 포함 '3':시간외 거래량 모두 제외 '4':장전시간외 거래량만 포함
    '''
    reader = Reader()
    query = {0: 'A005930', 1: ord('1'), 2: 20171231, 3: 20150101, 5: [0, 1, 2, 3, 4, 5, 8], 6: ord('m'), 8: ord('0'), 9: ord('0'), 10:ord('1')}
    chart_data = reader.query_stock_chart(query)
    print(chart_data)


if __name__ == '__main__':
    main()
