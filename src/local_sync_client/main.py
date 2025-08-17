
from config.config import ApplicationConfiguration
from file_watcher.file_watcher import File_watcher
from user.user import User


import threading



def main():

    print("Starting Local Sync Client...")
    print("Loading log in menu...")

    print("Loading user...")
    user_instance = User('asier')
    print(f"User loaded: {user_instance.config.USERNAME}")

    print("Wahtchdog Loading...")
    for path in user_instance.config.LOCAL_STORAGE_PATH_LIST:
        print(f"Watching path: {path}")
        file_watcher = File_watcher(path)
        file_watcher_thread = threading.Thread(target=file_watcher, args=(path,))
        file_watcher_thread.start()
    print("Watchdog threads started.")

    print("Local Sync Client is working...")

if __name__ == "__main__":
    main()