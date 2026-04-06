import pandas as pd
import sqlite3
import os
from utils.logger import Logger


# Class to manage conection with the sqlite database
class Sqlite():

    def __init__(self, db_path):
        self.db_path = db_path
        self._logger = Logger()
        self._init_db()
        self.data = self.generate_df()

    # Generates df with the ids of each db (local and cloud)
    def generate_df(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Do the select
        c.execute('''SELECT id FROM tracked_files''')
        conn.commit()
        # Before closin conection with the db store in a dataframe
        rows = c.fetchall()
        df = pd.DataFrame(data=rows)
        conn.close()
        return df
    
    # Bb generation method, only generated if not find 
    def _init_db(self):
        if os.path.exists(self.db_path) == False:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS tracked_files
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        path TEXT UNIQUE,
                        last_modified TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
            self._logger.print(f"Inited db on {self.db_path}")
            conn.commit()
            conn.close()
        

    