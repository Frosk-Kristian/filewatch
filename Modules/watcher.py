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
        # skips directory modifications as they are a side effect of other events within the directory and otherwise pollute logs/database with meaningless information
        if event.is_directory:
            return
        
        print(f"I saw something change: {event} (modified)")
        insert_db(event.src_path, "", "modify")

    def on_moved(self, event: FileSystemEvent) -> None:
        print(f"I saw something move: {event} (moved)")
        insert_db(event.src_path, event.dest_path, "move")

def watcher(dirs: dict[str, list[str]]):
    """
    Accepts a dictionary of directories, grouped by disk drive, and registers an observer to each drive to watch for file changes. 
    If all directories are on the same drive, just supply a dictionary with a single key-value pair. 
    The actual value of the key(s) shouldn't matter, as it's just used to group directories under the same observer.
    Args:
        dirs: dictionary with string disk drives as keys and lists of string directories as values
    Raises:
        ValueError: if dirs is empty
    """
    # checks if dictionary is empty
    if not dirs:
        raise ValueError("no valid directories provided!")

    # event handler instance
    handler = MyEventHandler()
    # list of observers
    observers = []

    # registers a new observer for each disk in the supplied list of directories
    for disk in dirs.keys():
        observer = Observer()

        # schedules the observer to watch each directory in dirs
        for dir in dirs[disk]:
            print(f"I will watch: {dir}")
            observer.schedule(handler, dir, recursive=True)
    
        observer.start()
        observers.append(observer)

    # runs until interrupted by the user (Ctrl+C)
    print("Watching for file changes, press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted, stopping...")
    finally:
        # signals to each thread to shut down (non-blocking)
        for observer in observers:
            observer.stop()
        # waits for each thread to actually finish (blocking)
        for observer in observers:
            observer.join()
