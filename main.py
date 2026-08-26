import sys, os
from collections import defaultdict
from Modules.watcher import watcher
from Modules.dbman import init_db

def group_by_disk(dirs: list[str]) -> dict[str, list[str]]:
    """
    Groups a list of directories by their disk drive letter.
    Args:
        dirs: list of string directories to be grouped
    Returns:
        dict: dictionary with disk drive letters as keys and lists of directories as values
    """
    grouped_dirs = defaultdict(list)

    # iterates through each directory and groups them by their drive
    # doesn't bother printing to avoid apearing erroneous due to disk appearing blank on Linux and MacOS, it does work (I have tested as such) but the drive letter just isn't displayed
    for dir in dirs:
        disk = os.path.splitdrive(dir)[0]
        grouped_dirs[disk].append(dir)
    
    return grouped_dirs

if __name__ == "__main__":
    # check for command line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <first_directory> <second_directory> ...")
        sys.exit(1)

    watched = [] # list of directories to monitor for file changes

    for i in range(1, len(sys.argv)):
        dir = sys.argv[i]
        if not os.path.isdir(dir):
            print(f"ERROR: \"{dir}\" is a file, not a directory!") if os.path.isfile(dir) else print(f"ERROR: no such directory \"{dir}\"!")
        else:
            watched.append(dir)

    try:
        init_db()
        watcher(group_by_disk(watched))
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
