"""A command line tool for managing Pype projects"""

import sys
import shutil
import os

def main():
    if len(sys.argv) != 3:
        print("Usage: plumber.py new <new_project_name>")
        sys.exit(1)

    source_folder = "template"
    new_project_name = sys.argv[2]

    print(f'\033[42m Plumber \033[0m creating project: \033[1m{new_project_name}\033[0m')

    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist.")
        sys.exit(1)
    
    destination_folder = os.path.join(os.path.dirname(source_folder), new_project_name)

    if os.path.exists(destination_folder):
        print(f"Error: Destination folder '{destination_folder}' already exists.")
        sys.exit(1)

    try:
        shutil.copytree(source_folder, destination_folder)
        print(f'\033[42m Plumber \033[0m \033[1m{new_project_name}\033[0m is created. Productive Coding!')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
