import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List

from user.user import User
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
import time
import threading


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class File_traker(metaclass=SingletonMeta):
    
    def __init__(self, user: User):
        self.user = user
        self.file_watchers = []
        self._init_db()

    def add_path_to_watch(self, path):
        self.file_watchers.append(File_watcher(path = path, event_handler = Whatchdog_event_handler(self)))
    
    def run_all(self):
        for watcher in self.file_watchers:
            file_watcher_thread = threading.Thread(target=watcher)
            file_watcher_thread.start()
    # TODO parar hilos bien
     
        
    # DB releated methotd

    def _init_db(self):
        conn = sqlite3.connect(self.user.config.APP_TRAKER_DB_FILE_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tracked_files
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE,
                    last_modified TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def update_file_record(self, filepath):
        conn = sqlite3.connect(self.user.config.APP_TRAKER_DB_FILE_PATH)
        c = conn.cursor()
        mod_time = datetime.fromtimestamp(Path(filepath).stat().st_mtime).isoformat()
        print('''INSERT OR REPLACE INTO tracked_files 
            (path, last_modified) 
            VALUES (?, ?)''', (str(filepath), mod_time))
        c.execute('''INSERT OR REPLACE INTO tracked_files 
                    (path, last_modified) 
                    VALUES (?, ?)''', (str(filepath), mod_time))

        conn.commit()
        conn.close()

# TODO Configurable whatch dog events
class Whatchdog_event_handler(FileSystemEventHandler):

    def __init__(self, traker:File_traker):
        super().__init__()
        self._traker = traker

    # def on_created(self, event: FileSystemEvent) -> None:
    #     print(event)

    def on_modified(self, event: FileSystemEvent) -> None:
        print(event)
        if (event.event_type == 'modified' and event.is_directory == False):
            self._traker.update_file_record(event.src_path)

    # def delete(self, event: FileSystemEvent) -> None:
    #     print(event)


# This is the file watcher class that will be used to watch the file system
class File_watcher:
        
    def __init__(self, path:str, event_handler:Whatchdog_event_handler):
        self.path = path
        self.event_handler = event_handler
    
    def __call__(self):
        self.run()
    
    # Run method that observe change every second 
    def run(self):
        observer = Observer()
        observer.schedule(self.event_handler, self.path, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()