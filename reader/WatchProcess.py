class WatchProcess:
    """
    This is an 'Abstract Class'(interface) for implementing concrete watch class.
    Each concrete watch class(WatchWithCreon, WatchWitheBest and etc) should be implemented based on this class.
    """
    def __init__(self):
        pass

    def watch(self, codes):
        raise NotImplementedError("Class %s doesn't implement a collect Method()" % (self.__class__.__name__))

