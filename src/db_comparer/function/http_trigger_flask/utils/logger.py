from datetime import datetime
from utils.singelton import SingletonMeta

# Class to centralize login system with timestamp
class Logger(metaclass=SingletonMeta):
    
    def __init__(self):
        pass

    def print(self, msg):
        print(f"{datetime.now().isoformat()} --- {msg}")

        