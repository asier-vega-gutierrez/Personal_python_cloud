import threading
import time
from http_manager.http_manager import Http_manager
from utils.logger import Logger

class File_uploader():

    def __init__(self, username):
        self.file_uploader_thread = None
        self.http_manager = Http_manager()
        self.username = username
        self.running = False
        self.logger = Logger()
        self.last_request_dt = None 

    def run(self):
        self.running = True
        self.file_uploader_thread = threading.Thread(target=self.request_upload_rutine)
        self.file_uploader_thread.start()
    
    def request_upload_rutine(self):
        self.last_request_dt = self.http_manager.request_ids(self.username)
        self.logger.print("File uploader has made a sucessful request")
            

    def stop(self):
        self.running = False
        if self.file_uploader_thread:
            self.file_uploader_thread.join()
    
