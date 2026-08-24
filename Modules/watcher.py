import time
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from .dbman import insert_db

class MyEventHandler(FileSystemEventHandler):
    """
    Event handler that looks for file system changes and inserts them into a database. 
    For the purpose of this snippet also prints the observed changes to stdout, this functionality would be removed in a production environment.
    """
    def on_created(self, event: FileSystemEvent) -> None:
        print(f"I see something new: {event} (created)")
        insert_db(event.src_path, "", "create")

    def on_deleted(self, event: FileSystemEvent) -> None:
        print(f"I no longer see: {event} (deleted)")
        insert_db(event.src_path, "", "delete")

    def on_modified(self, event: FileSystemEvent) -> None:
        print(f"I saw something change: {event} (modified)")
        insert_db(event.src_path, "", "modify")

    def on_moved(self, event: FileSystemEvent) -> None:
        print(f"I saw something move: {event} (moved)")
        insert_db(event.src_path, event.dest_path, "move")

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
