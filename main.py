import sys, os
from Modules.watcher import watcher

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

    if not watched:
        print("ERROR: no valid directories!")
        sys.exit(1)

    watcher(watched)
