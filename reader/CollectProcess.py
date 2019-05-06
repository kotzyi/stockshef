class CollectProcess:
    """
    This is an 'Abstract Class'(interface) for implementing concrete collect class.
    Each concrete collect class(CollectWithCreon, CollectWitheBest and etc) should be implemented based on this class.
    """
    def __init__(self):
        self.DAY = None
        self.MIN = None

    def collect(self, chart_class):
        raise NotImplementedError("Class %s doesn't implement a collect Method()" % (self.__class__.__name__))

    def interpolator(self, chart, num_day=4):
        """
        거래가 일어나지 않아 중간에 비어있는 데이터를 interpolation 하기 위한 함수
        :param chart:
        :return:
        """
        raise NotImplementedError("Class %s doesn't implement a collect Method()" % (self.__class__.__name__))

    def split_by_day(self, chart, num_day=1):
        """
        차트에서 원하는 날짜의 데이터(가장 최근의 날부터 - numdays 만큼) 스플릿해서 차트를 반환하는 함수
        :param chart: 주식 차트 데이터
        :param numdays: 원하는 날짜의 수
        :return:
        """
        raise NotImplementedError("Class %s doesn't implement a collect Method()" % (self.__class__.__name__))
