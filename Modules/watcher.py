import time

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

class MyEventHandler(FileSystemEventHandler):
    #def on_any_event(self, event: FileSystemEvent) -> None:
        #print(f"I saw something: {event}")

    def on_created(self, event: FileSystemEvent) -> None:
        print(f"I see something new: {event} (created)")

    def on_deleted(self, event: FileSystemEvent) -> None:
        print(f"I no longer see: {event} (deleted)")

    def on_modified(self, event: FileSystemEvent) -> None:
        print(f"I saw something change: {event} (modified)")

def watcher(dirs: list[str]):
    """
    Accepts a list of directories to be watched for file changes and schedules an observer to monitor them.
    Args:
        dirs: list of string directories to be monitored
    Raises:
        ValueError: if dirs is empty
    """
    # checks for empty lists
    if not dirs:
        raise ValueError("no valid directories provided!")
    
    handler = MyEventHandler()
    observer = Observer()

    # schedules the observer to watch each directory in dirs
    for dir in dirs:
        observer.schedule(handler, dir, recursive=True)
    
    observer.start()

    # runs until interrupted by the user (Ctrl+C)
    print("Watching for file changes, press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted, stopping...")
    finally:
        observer.stop()
        observer.join()
