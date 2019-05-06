from reader import LoginProcess
from reader import CollectProcess
from reader import WatchProcess
from reader import SaveProcess


class Reader:
    def __init__(self):
        self.login_process = LoginProcess
        self.collect_process = CollectProcess
        self.watch_process = WatchProcess
        self.save_process = SaveProcess

    def execute_login(self):
        self.login_process.login()

    def execute_collect(self):
        self.collect_process.collect()

    def execute_watch(self):
        self.watch_process.watch()

    def execute_save(self):
        self.save_process.save_history()
