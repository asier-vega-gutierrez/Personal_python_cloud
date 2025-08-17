
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

import time

# This is the file watcher evetn handler  
class WhatchdogEventHandler(FileSystemEventHandler):

    def on_created(self, event: FileSystemEvent) -> None:
        print(event)
    def on_modified(self, event: FileSystemEvent) -> None:
        print(event)
    def delete(self, event: FileSystemEvent) -> None:
        print(event)

# This is the file watcher class that will be used to watch the file system
class File_watcher:
        
    def __init__(self, path:str):
        self.path = path
    
    def __call__(self, path:str):
        self.run()
    
    # Runt method that observe change every 
    def run(self):
        event_handler = WhatchdogEventHandler()
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()