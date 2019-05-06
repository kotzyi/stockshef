from reader import Reader
from reader import LoginWithCreon
from reader import CollectWithCreon
from reader import WatchWithCreon
from reader import SaveWithPandas


class CreonReader(Reader):
    def __init__(self):
        self.login_process = LoginWithCreon
        self.collect_process = CollectWithCreon
        self.watch_process = WatchWithCreon
        self.save_process = SaveWithPandas
