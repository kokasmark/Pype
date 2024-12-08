"""A command line tool for managing Pype projects"""

import sys
import shutil
import subprocess
import os

def main():
    os.system("")

    source_folder = "template"
    action = sys.argv[1]

    if action == "new":
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
    if action == "build":
        folder = input(f'\033[42m Plumber \033[0m Pype Project to build: \033[1m').strip()
        print('\033[0m')

        if not os.path.isdir(folder):
            print(f'\033[41m Error: \033[0m {folder} does not exist.')
            return

        console = ""
        
        while console != "y" and console != "n":
            console = input(f'\033[42m Plumber \033[0m Pype console? (\33[5my\33[0m/\33[5mn\33[0m) \033[1m')
        print('\033[0m')

        # Clean previous builds
        dist_folder = os.path.join(folder, 'dist')
        build_folder = os.path.join(folder, 'build')
        spec_file = os.path.join(folder, 'app.spec')

        for path in [dist_folder, build_folder, spec_file]:
            if os.path.exists(path):
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)

        # Paths for PyInstaller
        app_file = os.path.join(folder, 'app.py')
        frontend_folder = os.path.join(folder, 'frontend')
        assets_folder = os.path.join(frontend_folder, 'assets')

        if not os.path.isfile(app_file):
            print(f'\033[41m Error: \033[0m {app_file} not found.')
            return

        # Build command
        pyinstaller_cmd = [
            'pyinstaller',
            '--noconfirm',
            '--clean',
            '--onefile',
            '--windowed',
            '--log-level', 'FATAL',
            '--python-option=-OO',
            '--add-data', f'{frontend_folder}{os.pathsep}frontend',
            '--add-data', f'{assets_folder}{os.pathsep}assets',
            '--distpath', f'{os.path.join(folder, "build")}',
            '--paths', os.getcwd(),
            '--hidden-import', 'pkg_resources',
            '--hidden-import', 'pkg_resources.extern',
            '--workpath', os.path.join(folder, 'build', 'temp'),
            f'--icon={ os.path.join(frontend_folder,"favicon.ico")}',
            app_file
        ]  
        
        if console == "y":
            pyinstaller_cmd.append('--console')
        try:
            subprocess.run(pyinstaller_cmd, check=True)
            print(f'\033[42m Success: \033[0m Build completed successfully.')
            temp_folder = os.path.join(folder, 'build', 'temp')
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)

        except subprocess.CalledProcessError as e:
            print(f'\033[41m Error: \033[0m Build failed: {str(e)}')

    

if __name__ == "__main__":
    main()
