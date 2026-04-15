
from azure.storage.blob import BlobServiceClient

from utils.singelton import SingletonMeta
from config.config import ApplicationConfiguration

class Blob_manager(metaclass=SingletonMeta):
    
    def __init__(self):
        self.config = ApplicationConfiguration()
        self.blob_service_client = BlobServiceClient.from_connection_string(self.config.APP_CONNECTION_STRING)
        self.container_name = "dbcomparer-sc-upload"

    def save_file_to_container(self, file, file_name):
        container_client = self.blob_service_client.get_container_client(container=self.container_name)
        container_client.upload_blob(name=file_name, data=file)
        
    def get_file_from_container(self, file_name):
        container_client = self.blob_service_client.get_container_client(container=self.container_name)
        container_client.download_blob(blob=file_name)