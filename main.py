import sys, os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <first_directory> <second_directory> ...")
        sys.exit(1)

    watched = []

    for i in range(1, len(sys.argv)):
        dir = sys.argv[i]
        if not os.path.isdir(dir):
            print(f"ERROR: invalid directory \"{dir}\"!")
        else:
            watched.append(dir)

    if not watched:
        print("ERROR: no valid directories!")
        sys.exit(1)
