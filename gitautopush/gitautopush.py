import sys
from subprocess import call, check_output, STDOUT
import os
from time import sleep
import argparse
import shutil as sh
from datetime import datetime

DESCRIPTION = ("Automatically syncronize and push a file/foder to GitHub, "
               "optionally running nbconvert in the process.\n\n"
               "Useful for teaching with one of more files that you populate "
               "as you go along. This tool will automatically sync "
               "changes that you make and push them to GitHub so that "
               "students can use it as a reference.")
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("path", help="Path to the notebook or folder to be pushed.")
parser.add_argument("--sleep", default=10, help="Time to wait (in seconds) before checking for updates.")
parser.add_argument("--out-name", default=None, help="A new name for the file/folder to be pushed to GitHub.")
parser.add_argument("--no-push", dest='do_push', action='store_false', help="Prevent an attempt to push the new file to GitHub.")
parser.add_argument("--nbconvert-to", default=None, help="Attempt to run `nbconvert` on the file. Accepts any nbconvert argument used with `--to`.")
parser.add_argument("--out-path", default=None, help="The location to place the output folder. Default is the current directory.")
parser.set_defaults(no_push=False)


def main():
    # Parse args
    args = parser.parse_args()
    in_path = args.path
    this_sleep = int(args.sleep)
    out_name = str(args.out_name) if args.out_name is not None else None
    nbconvert_to = str(args.nbconvert_to) if args.nbconvert_to is not None else None
    out_path = str(args.out_path) if args.out_path is not None else None
    do_push = bool(args.do_push)

    # Check out path and naming
    out_path = os.path.curdir if out_path is None else out_path


    # Checks
    if not os.path.exists(in_path):
        raise ValueError("Input path doesn't exist, double-check your path")
    print("Observing path: {}".format(in_path))

    if nbconvert_to is None:
        copy = sh.copytree if os.path.isdir(in_path) else sh.copy
    # If we're just copying, then keep the same base name unless another is specified
    # If we're using nbconvert, then it'll take care of the renaming so skip this part
    # However we still need the output path for nbconvert
    new_name = os.path.basename(in_path) if out_name is None else out_name
    new_path = os.path.join(out_path, new_name)


    # --- Main loop ---
    ii = 1
    while True:
        if nbconvert_to is None:
            copy(in_path, new_path)
        else:
            # nbconvert will tell us the name of the output file
            nbconvert_dir = new_path if os.path.isdir(new_path) else os.path.dirname(new_path)
            new_path = nbconvert(in_path, nbconvert_dir, nbconvert_to)
            new_name = os.path.basename(new_path)

        if do_push:
            out = add_and_commit(new_path)
            if out == 0:
                call(('git', 'push'))
                print('\n\n---\n\n')
                print('Notebook synced (Num: {})'.format(ii))
                ii += 1
        sleep(this_sleep)

def nbconvert(path, nbconvert_dir, to):
    output = check_output(['jupyter', 'nbconvert', '--to', to, '--output-dir', nbconvert_dir, '-y', path], stderr=STDOUT)
    path_new = output.decode().split('bytes to ')[-1].strip()
    return path_new

def add_and_commit(path):
    # Check if file is in git, if not then add it:
    out = call(['git', 'ls-files', '--error-unmatch', path])
    msg = "new file: {}" if out == 1 else 'file synced: {}'
    msg = msg.format(os.path.basename(path))
    call(['git', 'add', path])
    out = call(['git', 'commit', '-m', msg])
    return out

if __name__ == '__main__':
    main()
