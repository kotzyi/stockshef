from reader import CreonPublish
from reader import CreonAPI


class CreonWatchPublish(CreonPublish):
    def __init__(self):
        super().__init__('watcher', CreonAPI.obj_StockCur, CreonPublish)
