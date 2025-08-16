
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

import time

class WhatchdogEventHandler(FileSystemEventHandler):

    def on_created(self, event: FileSystemEvent) -> None:
        print(event)
    def on_modified(self, event: FileSystemEvent) -> None:
        print(event)
    def delete(self, event: FileSystemEvent) -> None:
        print(event)

class File_watcher:
        
    def __init__(self):
        self.path = "/home/asier/Personal_cloud/local_storage_1"
    
    def __call__(self):
        self.run()
    
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