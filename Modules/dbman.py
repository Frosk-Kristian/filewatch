import sqlite3
from pathlib import Path

# Path to database file, will be set in init_db
db_path = ""

def insert_db(source: str, destination: str, update_type: str):
    """
    Inserts a new file update into the database.
    Args:
        source: path to the file that was updated
        destination: new path of the file in the event that it was moved or renamed
        update_type: type of file update (create, delete, modify, move)
    Raises:
        ValueError: if db_path is empty (i.e. init_db() has not been called)
    """
    if not db_path:
        raise ValueError("Database path not set, call init_db() before inserting into database.")

    with sqlite3.connect(db_path, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO file_updates(source, destination, update_type) VALUES (?, ?, ?)", (source, destination, update_type))

def init_db(db: str = "file_changes.db"):
    """
    Initialises SQLite database and creates the file_updates table if one does not already exist.
    Args:
        db: database filename (defaults to "file_changes.db")
    """
    global db_path
    db_path = Path(__file__).parent.parent / "Data" / db

    with sqlite3.connect(db_path) as conn:
        # enables write ahead logging mode
        conn.execute("PRAGMA journal_mode=WAL")
        cursor = conn.cursor()

        # creates the file_updates table if it doesn't already exist, with the following columns:
        # id: unique identified for each update
        # source: path of the file that was updated
        # destination: new path of the file in the event that it was moved or renamed
        # update_type: type of file update (create, delete, modify, move)
        # timestamp: time of the update
        # sync_status: indicates whether the update has been synced to server (0 = not synced, 1 = synced, 2 = failed to sync)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                destination TEXT,
                update_type TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                sync_status INTEGER DEFAULT 0
            )
        ''')

        # creates indexes on the sync_status and timestamp columns to improve query performance
        # not really within the scope of this snippet but I felt it would be good practice to include seeing as the idea is that a separate application would be querying this db to sync changes with a server
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_sync_status ON file_updates(sync_status)''')
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_timestamp ON file_updates(timestamp)''')
