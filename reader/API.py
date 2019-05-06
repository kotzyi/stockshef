class API:
    """
    This is an 'Abstract Class'(interface) for implementing API class.
    Each API(creon, eBest and etc) should be implemented based on this class.
    """

    def __init__(self):
        self.ERROR = 1
        self.OK = 0

    def get_stock_code_list(self):
        raise NotImplementedError("Class %s doesn't implement a get_stock_chart Method()" % (self.__class__.__name__))

    def connect(self):
        raise NotImplementedError("Class %s doesn't implement a is_connect Method()" % (self.__class__.__name__))

    def login(self):
        raise NotImplementedError("Class %s doesn't implement a login Method()" % (self.__class__.__name__))


