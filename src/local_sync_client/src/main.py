
from user.user import User
from file_traker.file_traker import File_traker
from utils.logger import Logger
from utils.signal_handler import Signalhandler

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
    file_traker = File_traker(user)
    for path in user.config.LOCAL_STORAGE_PATH_LIST:
        file_traker.add_path_to_watch(path)
    logger.print("Starting to Watch...")
    file_traker.run_all()
    logger.print("Whatching user file routes")

    logger.print("Local Sync Client is working...")

    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     logger.print("Received shutdown signal. Exiting...")
    # finally:
    #     logger.print("Stopping file tracker...")
    #     #file_traker.stop_all()
    #     logger.print("Local Sync Client stopped.")


if __name__ == "__main__":
    main()