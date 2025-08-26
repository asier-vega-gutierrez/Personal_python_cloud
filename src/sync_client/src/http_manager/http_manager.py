import requests 
import pandas as pd
from utils.logger import Logger

# Class that mannged all the http traffic of the sync_client
class Http_manager():

    def __init__(self):
        self.type = "local"
        self.logger = Logger()

    # Execute get to the compare_bd api
    def get_ids(self, url, username):
        response = requests.get(f'{url}compare?username={username}')
        if (response.status_code == 200):
            self.logger.print("HTTP Sucessful get")
            data = response.json()
            return pd.DataFrame(eval(data))

    # Execute post to the compare_db api
    def post_db(self, url, db_path, username):
        db_file = {"file": open(db_path, "rb")}
        response = requests.post(f'{url}upload?type={self.type}&username={username}', files=db_file)
        if (response.status_code == 200):
            self.logger.print("HTTP Sucessful post")    
