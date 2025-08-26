import os
from utils.yaml_reader import YamlReader
from utils.singelton import SingletonMeta

class ApplicationConfiguration(metaclass=SingletonMeta):
    
    def __init__(self, username:str):

        # APPLICATION CONFIGURATION
        self.APP_CONFIG_FILE_PATH = './config/config.yaml'
        self.APP_TRAKER_DB_FILE_PATH = './db/tracker.db'
        self.APP_COMPARE_BD_URL = "http://localhost:5000/"

        self.reader = YamlReader(self.APP_CONFIG_FILE_PATH)
        self.config = self.reader.get_config_username('asier') 

        # USER CONFIG 
        self.USERNAME = self.config['username']
        self.EMAIL = self.config['email']
        self.KEY_PATH = self.config['key_location']
        self.LOCAL_STORAGE_PATH_LIST = self.config['local_sotorage_paths']
