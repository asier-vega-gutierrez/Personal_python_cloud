
from config.config import ApplicationConfiguration
from file_watcher.file_watcher import File_watcher

import threading


class user():
    def __init__(self):
        self.config = ApplicationConfiguration()
    

def main():
    file_watcher_thread = threading.Thread(target=File_watcher())
    file_watcher_thread.start()

if __name__ == "__main__":
    main()