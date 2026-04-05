import os
from utils.yaml_reader import YamlReader
from utils.singelton import SingletonMeta
from dotenv import load_dotenv

class ApplicationConfiguration(metaclass=SingletonMeta):
    
    def __init__(self, username:str):

        # APPLICATION CONFIGURATION
        load_dotenv()
        self.APP_CONFIG_FILE_PATH = './config/config.yaml'
        self.APP_TRAKER_DB_FILE_PATH = './db/tracker.db'
        self.APP_COMPARE_BD_URL = "http://localhost:5000/"
        self.APP_CONNECTION_STRING = os.environ['AZURE_CONN_STRING']

        self.reader = YamlReader(self.APP_CONFIG_FILE_PATH)
        self.config = self.reader.get_config_username(username) 

        # USER CONFIG 
        self.USERNAME = self.config['username']
        self.EMAIL = self.config['email']
        self.KEY_PATH = self.config['key_location']
        self.LOCAL_STORAGE_PATH_LIST = self.config['local_sotorage_paths']
        self.CONTAINER_NAME = self.config['username'] + "-container"