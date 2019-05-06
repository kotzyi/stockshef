class SaveProcess:
    """
    This is an 'Abstract Class'(interface) for implementing concrete save class.
    Each concrete save class(SaveWithPandas, SaveWithMongoDB and etc) should be implemented based on this class.
    """
    def __init__(self):
        self.save_path = None

    def save_history(self, chart, code):
        raise NotImplementedError("Class %s doesn't implement a save Method()" % (self.__class__.__name__))

    def save_realtime(self, chart, code):
        raise NotImplementedError("Class %s doesn't implement a save Method()" % (self.__class__.__name__))
