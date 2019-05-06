class LoginProcess:
    """
    This is an 'Abstract Class'(interface) for implementing concrete login class.
    Each concrete login class(LoginWithCreon, LoginWitheBest and etc) should be implemented based on this class.
    """
    def __init__(self):
        raise NotImplementedError("Class %s doesn't implement a login Method()" % (self.__class__.__name__))

    def login(self):
        raise NotImplementedError("Class %s doesn't implement a login Method()" % (self.__class__.__name__))
