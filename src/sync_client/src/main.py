
from user.user import User
from file_traker.file_tracker import File_traker
from utils.logger import Logger
from file_uploader.file_uploader import File_uploader

import  time
import signal

def main():

    logger = Logger()

    logger.print("Starting Local Sync Client...")
    logger.print("Loading log in menu...")

    logger.print("Loading user...")
    user = User('asier')
    logger.print(f"User loaded: {user.config.USERNAME}")

    logger.print("Starting File Traker...")
    file_traker = File_traker(db_path = user.config.APP_TRAKER_DB_FILE_PATH)
    logger.print("Adding path to watch...")
    file_traker.add_paths_to_watch(user.config.LOCAL_STORAGE_PATH_LIST)
    logger.print("Starting to watch...")
    file_traker.run_all()
    logger.print("Whatching user file routes")

    file_uploader = File_uploader(user.config.USERNAME)
    file_uploader.run()

    logger.print("Local Sync Client is working...")

    try:
        while True:
            # cada minuto se relaiza una llamada para comparar las bases de datos
            # se descarga los cmabio
            # se suben los archivos a la nube
            time.sleep(60)
    except KeyboardInterrupt:
        logger.print("Received shutdown signal. Exiting...")
    finally:
        logger.print("Stopping file tracker...")
        file_traker.stop_all()
        logger.print("Local Sync Client stopped.")


if __name__ == "__main__":
    main()