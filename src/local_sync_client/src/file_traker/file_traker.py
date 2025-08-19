import sqlite3
from pathlib import Path
from datetime import datetime
import time
import threading
import os 

from user.user import User
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from utils.singelton import SingletonMeta




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

    def insert_replace_file_record(self, filepath):
        conn = sqlite3.connect(self.user.config.APP_TRAKER_DB_FILE_PATH)
        c = conn.cursor()
        mod_time = datetime.fromtimestamp(Path(filepath).stat().st_mtime).isoformat()
        c.execute('''INSERT OR REPLACE INTO tracked_files 
                    (path, last_modified) 
                    VALUES (?, ?)''', (str(filepath), mod_time))
        print(f"Inserted to db: {filepath}")
        conn.commit()
        conn.close()
    
    def delete_file_record(self, filepath):
        conn = sqlite3.connect(self.user.config.APP_TRAKER_DB_FILE_PATH)
        c = conn.cursor()
        c.execute('''DELETE FROM tracked_files 
                    WHERE path = ?''', (str(filepath),))
        if c.rowcount > 0:
            print(f"Deleted from db: {filepath}")
        else:
            print(f"No record found for: {filepath}")
        conn.commit()
        conn.close()

# file events detector for File Watchers
class Whatchdog_event_handler(FileSystemEventHandler):

    def __init__(self, traker:File_traker):
        super().__init__()
        self._traker = traker

    # Detect modifi event only files
    def on_modified(self, event: FileSystemEvent) -> None:
        if (event.is_directory == False):
            print(event)
            self._traker.insert_replace_file_record(event.src_path)

    # Detect delete events only files
    def on_deleted(self, event: FileSystemEvent) -> None:
        if (event.is_directory == False):
            print(event)
            self._traker.delete_file_record(event.src_path)
    
    # Detect rename events (move are detected with on_deleted and on_creted)
    def on_moved(self, event: FileSystemEvent) -> None:
        if (event.is_directory == False):
            print(event)
            self._traker.insert_replace_file_record(event.dest_path)
            self._traker.delete_file_record(event.src_path)
    
    # Detect create events, if the file has 0 bits is not traked 
    def on_created(self, event: FileSystemEvent):
        if (event.is_directory == False):
            if(os.path.getsize(event.src_path) > 0):
                print(event)
                self._traker.insert_replace_file_record(event.src_path)


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

        # TODO improve execution
        try:
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()