import os

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ApplicationConfiguration(metaclass=SingletonMeta):
    
    def __init__(self):

        # USER CONFIG 
        self.USERNAME = 'default_username'
        self.EMAIL = 'default_email'
        self.KEY_PATH = 'default_key_path'
        self.LOCAL_STORAGE_PATH ='default_local_storage_path'

        # APPLICATION CONFIGURATION
        self.USER_CONFIG_FILE = '/home/asier/Personal_cloud/src/local_sync_client/config/config.yaml'