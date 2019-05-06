from win32com import client


class CreonPublish:
    def __init__(self, name, obj, event):
        self.name = name
        self.obj = obj
        self.event = event
        self.is_subscribe = False

    def subscribe(self, var, caller):
        if self.is_subscribe:
            self.unsubscribe()

        if (len(var) > 0):
            self.obj.SetInputValue(0, var)

        handler = client.WithEvents(self.obj, self.event)
        handler.set_params(self.obj, self.name, caller)
        self.obj.subscribe()
        self.is_subscribe = True

    def unsubscribe(self):
        if self.is_subscribe:
            self.obj.unsubscribe()
        self.is_subscribe = False
