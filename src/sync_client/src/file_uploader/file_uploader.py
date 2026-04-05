import threading
import time
import pandas as pd
import os
import sqlite3
from http_manager.http_manager import Http_manager
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

from utils.singelton import SingletonMeta
from utils.logger import Logger
from config.config import ApplicationConfiguration


# Class that manage:
# the post of the squlite local db to the compare_db api
# the get of the id diference of the compare_db api
class File_uploader(metaclass=SingletonMeta):

    def __init__(self):
        self.config = ApplicationConfiguration()
        self.file_uploader_thread = None
        self.running = False
        self.last_request_dt_ids = None 
        self.http_manager = Http_manager()
        self._logger = Logger()
        

    # Calling this executes a bakcgroud task that get the db diference id from the compare_bd api
    def run(self):
        self.running = True
        self.file_uploader_thread = threading.Thread(target=self._post_get_runtine)
        self.file_uploader_thread.start()
    
    # Executen the request via htt_manager
    def _post_get_runtine(self):
        self.http_manager.post_db(self.config.APP_COMPARE_BD_URL, self.config.APP_TRAKER_DB_FILE_PATH, self.config.USERNAME)
        self.last_request_dt_ids = self.http_manager.get_ids(self.config.APP_COMPARE_BD_URL, self.config.USERNAME)
        #print(self.last_request_dt_ids)
        if(self.last_request_dt_ids.empty == False):
            self._upload_files()

    # Stops the backgroun task
    def stop(self):
        self.running = False
        if self.file_uploader_thread:
            self.file_uploader_thread.join()

    # Executes the upload to azure blob of the corresponding files TODO generate my own container if it doesn't exists for that username
    def _upload_files(self):
        # Set client to access azure storage container
        blob_service_client = BlobServiceClient.from_connection_string(self.config.APP_CONNECTION_STRING)
        # Get the container client 
        container_client = blob_service_client.get_container_client(container=self.config.CONTAINER_NAME)
        # Get filepaths
        file_apth_dt = self._get_file_paths()
        file_paths = (file_apth_dt["path"]).tolist()
        # Upload the files
        for file_path in file_paths:
            with open(file_path, "r") as fl :
                data = fl.read()
                try:
                    container_client.upload_blob(name=str(file_path).strip("/"), data=data)
                    self._logger.print(f"Data have been sent to cloud")
                except ResourceExistsError:
                    pass

    # Gets the actual files paths of the files that ahs to be uploadad TODO move this to sql file (crete it)
    def _get_file_paths(self):
        conn = sqlite3.connect(self.config.APP_TRAKER_DB_FILE_PATH)
        # Extract IDs from the DataFrame
        ids_list = self.last_request_dt_ids.iloc[:,0].tolist()
        # Create placeholders for SQL query
        placeholders = ','.join('?' * len(ids_list))
        # Query the database for file paths matching the IDs
        query = f'''SELECT id, path, last_modified 
                    FROM tracked_files 
                    WHERE id IN ({placeholders})'''
        dt = pd.read_sql_query(query, conn, params=ids_list)
        conn.close()
        return dt