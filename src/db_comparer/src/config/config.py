import os
from utils.singelton import SingletonMeta

class ApplicationConfiguration(metaclass=SingletonMeta):
    
    def __init__(self, username:str):

        # APPLICATION CONFIGURATION
        self.APP_RECEIVED_DB_PATH= f'./upload/{username}_received.db'
        self.APP_STORED_DB_PATH = f'./upload/{username}_stored.db'