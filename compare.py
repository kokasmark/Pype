import os
import hashlib
from datetime import datetime

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def compare_files(dev_folder, pkg_folder):
    dev_files = os.listdir(dev_folder)

    for filename in dev_files:
        print("")
        dev_file = os.path.join(dev_folder, filename)
        pkg_file = os.path.join(pkg_folder, filename)

        if os.path.isdir(dev_file):
            if filename in ['template', 'frontend']:
                compare_files(dev_file, pkg_file)
            continue

        if os.path.exists(pkg_file):
            dev_hash = hash_file(dev_file)
            pkg_hash = hash_file(pkg_file)

            if dev_hash != pkg_hash:
                print(f"\33[31m{filename} ❌ Different\33[0m")
                dev_time = os.path.getmtime(dev_file)
                pkg_time = os.path.getmtime(pkg_file)

                if dev_time > pkg_time:
                    print(f"\t\33[94mDevelopment\33[0m version of {filename} is newer.")
                else:
                    print(f"\t\33[94mPackage\33[0m version of {filename} is newer.")
            else:
                print(f"\33[32m{filename} ✔️ Same\33[0m")
        else:
            print(f"\33[31m{filename} ❌ Missing in the package folder.\33[0m")


if __name__ == "__main__":
    os.system("")
    DEV_FOLDER = "development"
    PACKAGE_FOLDER = "package/src/Pype"

    compare_files(DEV_FOLDER, PACKAGE_FOLDER)
    input("Comparison complete.")