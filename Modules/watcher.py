import time

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        print(f"I saw something: {event}")

    def on_created(self, event: FileSystemEvent) -> None:
        print(f"I see something new: {event} (created)")

    def on_deleted(self, event: FileSystemEvent) -> None:
        print(f"I no longer see: {event} (deleted)")

def watcher(dirs: list[str]):
    if not dirs:
        print("ERROR: nothing to watch!")
        return
    
    handler = MyEventHandler()
    observer = Observer()

    for dir in dirs:
        print(f"I will watch: \"{dir}\"")
        observer.schedule(handler, dir, recursive=True)
    
    print("Watching...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted, stopping...")
    finally:
        observer.stop()
        observer.join()
