import sys
from subprocess import call, check_output
import os
from time import sleep
import argparse
import shutil as sh
from datetime import datetime

DESCRIPTION = ("Automatically syncronize and push a file/foder to GitHub.\n"
               "Useful for teaching with one of more files that you populate "
               "as you go along. This tool will automatically sync "
               "changes that you make and push them to GitHub so that "
               "students can use it as a reference.")
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("path", help="Path to the notebook or folder to be pushed.")
parser.add_argument("--sleep", default=15, help="Time to wait (in seconds) before checking for updates.")
parser.add_argument("--rename", default=None, help="A new name for the file/folder to be pushed to GitHub.")

def main():
    args = parser.parse_args()

    path = args.path
    this_sleep = int(args.sleep)
    rename = str(args.rename) if args.rename is not None else None
    newname = os.path.basename(path) if rename is None else rename
    new_path = os.path.join('.', newname)
    if not os.path.exists(path):
        raise ValueError("Path doesn't exist, double-check your path")

    copy = sh.copytree if os.path.isdir(path) else sh.copy
    if not os.path.exists(new_path):
        print('Adding new path: {}'.format(new_path))
        copy(path, new_path)
        call(['git', 'add', new_path])
        call(['git', 'commit', '-m', '"new path: {}"'.format(newname)])

    ii = 1
    while True:
        sh.copy(path, new_path)
        print('\n\n---\n\n')
        out = call(('git', 'commit', '-am', "update: {:%x %X}".format(datetime.now())))
        if out == 0:
            call(('git', 'push'))
            print('Notebook synced (Num: {})'.format(ii))
            ii += 1
        sleep(this_sleep)


if __name__ == '__main__':
    main()
