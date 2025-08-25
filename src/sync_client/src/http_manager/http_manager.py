import requests 
import pandas as pd
import json

class Http_manager():

    def __init__(self):
        pass

    def request_ids(self, username):
        request = requests.get(f'http://localhost:5000/compare?username={username}')
        data = request.json()
        return pd.DataFrame(eval(data))

    def post_db(self, db_path):
        pass
