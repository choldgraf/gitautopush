import sys
from subprocess import call, check_output
import os
from time import sleep
import argparse
import shutil as sh
from datetime import datetime

DESCRIPTION = ("Automatically syncronize and push a file to GitHub.\n"
               "Useful for teaching with a file that you populate "
               "as you go along. This tool will automatically sync "
               "changes that you make and push them to GitHub so that "
               "students can use it as a reference")
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("path", help="Path to the notebook to be pushed.")
parser.add_argument("--sleep", default=15, help="Time to wait (in seconds) before checking for updates.")
   
    
def main():
    args = parser.parse_args()

    path = args.path
    this_sleep = int(args.sleep)
    
    name = os.path.basename(path)
    new_path = os.path.join('.', name)
    if not os.path.exists(path):
        raise ValueError("Notebook doesn't exist, double-check your path")

    if not os.path.exists(new_path):
        print('Adding new file: {}'.format(new_path))
        sh.copy(path, new_path)
        call(['git', 'add', new_path])
        call(['git', 'commit', '-m', '"new file: {}"'.format(name)])
    
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