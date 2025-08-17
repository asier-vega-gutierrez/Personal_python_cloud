import os
from utils.yaml_reader import YamlReader

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ApplicationConfiguration(metaclass=SingletonMeta):
    
    def __init__(self, username:str):

        # APPLICATION CONFIGURATION
        self.USER_CONFIG_FILE = '/home/asier/Personal_cloud/src/local_sync_client/config/config.yaml'

        self.reader = YamlReader(self.USER_CONFIG_FILE)
        self.config = self.reader.get_config_username('asier') 

        # USER CONFIG 
        self.USERNAME = self.config['username']
        self.EMAIL = self.config['email']
        self.KEY_PATH = self.config['key_location']
        self.LOCAL_STORAGE_PATH_LIST = self.config['local_sotorage_paths']
