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
from utils.logger import Logger



# Class that mannage the trak system of local app
# contain multiple file_whatcer that controls each one a file system path
# manage the execution by threading
class File_traker(metaclass=SingletonMeta):
    
    def __init__(self, db_path):
        self.file_watchers = []
        self.file_watchers_thread = []
        self.db_path = db_path
        self._logger = Logger()
        self._init_db()

    # Method to add path, this add file_wather objetc to the list of file_watchers of file_traker
    def add_paths_to_watch(self, paths):
        for path  in paths:
            self.file_watchers.append(File_watcher(path = path, event_handler = Whatchdog_event_handler(self)))
    
    # Method to run all the whatcher, each one on a thread
    def run_all(self):
        for watcher in self.file_watchers:
            self.file_watchers_thread.append(threading.Thread(target=watcher))
        for thread in self.file_watchers_thread:
            thread.start()
    
    # Method to stop all the file watchers and its thread
    def stop_all(self):
        for watcher in self.file_watchers:
            watcher.stop()
        for thread in self.file_watchers_thread:
            thread.join() 
        self.file_watchers_thread.clear()

        
    # Bb generation method, only generated if not present 
    def _init_db(self):
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

    # Inserts or replace in the db a route
    def insert_replace_file_record(self, filepath):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        mod_time = datetime.fromtimestamp(Path(filepath).stat().st_mtime).isoformat()
        c.execute('''INSERT OR REPLACE INTO tracked_files 
                    (path, last_modified) 
                    VALUES (?, ?)''', (str(filepath), mod_time))
        self._logger.print(f"Inserted to db: {filepath}")
        conn.commit()
        conn.close()
    
    # Delete a route from the db
    def delete_file_record(self, filepath):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''DELETE FROM tracked_files 
                    WHERE path = ?''', (str(filepath),))
        if c.rowcount > 0:
            self._logger.print(f"Deleted from db: {filepath}")
        else:
            self._logger.print(f"No record found for: {filepath}")
        conn.commit()
        conn.close()

# Class that contain al the event listener for the file_watcher
class Whatchdog_event_handler(FileSystemEventHandler):

    def __init__(self, traker:File_traker):
        super().__init__()
        self._traker = traker
        self._logger = Logger()

    # Detect modifi event only files
    def on_modified(self, event: FileSystemEvent) -> None:
        if (event.is_directory == False):
            self._logger.print(event)
            self._traker.insert_replace_file_record(event.src_path)

    # Detect delete events only files
    def on_deleted(self, event: FileSystemEvent) -> None:
        if (event.is_directory == False):
            self._logger.print(event)
            self._traker.delete_file_record(event.src_path)
    
    # Detect rename events (move are detected with on_deleted and on_creted)
    def on_moved(self, event: FileSystemEvent) -> None:
        if (event.is_directory == False):
            self._logger.print(event)
            self._traker.insert_replace_file_record(event.dest_path)
            self._traker.delete_file_record(event.src_path)
    
    # Detect create events, if the file has 0 bits is not traked 
    def on_created(self, event: FileSystemEvent):
        if (event.is_directory == False):
            if(os.path.getsize(event.src_path) > 0):
                self._logger.print(event)
                self._traker.insert_replace_file_record(event.src_path)


# Class the observe a file system path 
# uses a event handler that is common for every file_wathcer
class File_watcher:
        
    def __init__(self, path:str, event_handler:Whatchdog_event_handler):
        self.path = path
        self.event_handler = event_handler
        self.observer = None
        self.running = False
    
    def __call__(self):
        self.run()
    
    # Run method that observe change on the file_wather path
    def run(self):
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()
        self.running = True
    
    # Stop method
    def stop(self):
        self.observer.stop()
        self.running = False
