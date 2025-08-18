
from user.user import User
from file_traker.file_traker import File_traker

import threading



def main():

    print("Starting Local Sync Client...")
    print("Loading log in menu...")

    print("Loading user...")
    user = User('asier')
    print(f"User loaded: {user.config.USERNAME}")

    print("Starting File Traker...")
    file_traker = File_traker(user)
    for path in user.config.LOCAL_STORAGE_PATH_LIST:
        file_traker.add_path_to_watch(path)
    print("Starting to Watch...")
    file_traker.run_all()

    print("Local Sync Client is working...")

if __name__ == "__main__":
    main()