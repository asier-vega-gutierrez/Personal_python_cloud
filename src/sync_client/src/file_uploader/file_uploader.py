import threading
import time
import pandas as pd
from http_manager.http_manager import Http_manager

from utils.singelton import SingletonMeta
from config.config import ApplicationConfiguration


# Class that manage:
# the post of the squlite local db to the compare_db api
# the get of the id diference of the compare_db api
class File_uploader(metaclass=SingletonMeta):

    def __init__(self):
        self.config = ApplicationConfiguration()
        self.file_uploader_thread = None
        self.running = False
        self.last_request_dt = None 
        self.http_manager = Http_manager()
        

    # Calling this executes a bakcgroud task that get the db diference id from the compare_bd api
    def run(self):
        self.running = True
        self.file_uploader_thread = threading.Thread(target=self._post_get_runtine)
        self.file_uploader_thread.start()
    
    # Executen the request via htt_manager
    def _post_get_runtine(self):
        self.http_manager.post_db(self.config.APP_COMPARE_BD_URL, self.config.APP_TRAKER_DB_FILE_PATH, self.config.USERNAME)
        self.last_request_dt = self.http_manager.get_ids(self.config.APP_COMPARE_BD_URL, self.config.USERNAME)

    # Stops the backgroun task
    def stop(self):
        self.running = False
        if self.file_uploader_thread:
            self.file_uploader_thread.join()

    def upload_files():
        pass

    
