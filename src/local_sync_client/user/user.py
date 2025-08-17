
from config.config import ApplicationConfiguration


class User():

    def __init__(self, username:str):
        self.config = ApplicationConfiguration(username=username)