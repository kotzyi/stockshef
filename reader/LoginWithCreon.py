from reader import LoginProcess
from reader import CreonAPI
import sys


class LoginWithCreon(LoginProcess):
    def __init__(self):
        self.api = CreonAPI

    def login(self):
        #Check
        if self.api.login() == self.api.ERROR:
            sys.exit(1)

        if self.api.connect() == self.api.ERROR:
            sys.exit(1)

