import os
from utils.singelton import SingletonMeta

class ApplicationConfiguration(metaclass=SingletonMeta):
    
    def __init__(self, username:str):

        # APPLICATION CONFIGURATION
        self.APP_UPLOAD_FOLDER = './upload'
        self.APP_RECEIVED_DB_PATH = f'./upload/{username}_local.db'
        self.APP_STORED_DB_PATH = f'./upload/{username}_cloud.db'