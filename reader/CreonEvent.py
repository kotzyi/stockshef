class CreonEvent:
    """
    This is an 'Abstract Class'(interface) for implementing CreonEvent class.
    Each Creon Event with publish class should be implemented based on this class.
    """

    def set_params(self, client, name, caller):
        self.client = client  # CP 실시간 통신 object
        self.name = name  # 서비스가 다른 이벤트를 구분하기 위한 이름
        self.caller = caller  # callback 을 위해 보관

    def on_received(self):
        raise NotImplementedError("Class %s doesn't implement a on_received method()" % (self.__class__.__name__))
