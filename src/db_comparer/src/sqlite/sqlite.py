import pandas as pd
import sqlite3


# Class to manage conection with the sqlite database
class Sqlite():

    def __init__(self, db_path):
        self.db_path = db_path
        self.data = self.generate_df()

    def generate_df(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Do de select
        c.execute('''SELECT id FROM tracked_files''')
        conn.commit()
        # Before closin conection with the db store in a dataframe
        rows = c.fetchall()
        df = pd.DataFrame(data=rows)
        conn.close()
        return df
        

    