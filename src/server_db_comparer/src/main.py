from config.config import ApplicationConfiguration
from sqlite.sqlite import Sqlite
import pandas as pd

def main():
    # need to receive the db from local_sync_client with the db_file_name as username
    # need to receive the db from cloud_sotrage with the db_file_name as username

    config = ApplicationConfiguration('asier')

    received_db = Sqlite(config.APP_RECEIVED_DB_PATH)
    stored_db = Sqlite(config.APP_STORED_DB_PATH)

    ids_to_uploada = pd.DataFrame(data = (set(received_db.data[0].values) - set(stored_db.data[0].values)) ) 
    print(ids_to_uploada)

if __name__ == "__main__":
    main()