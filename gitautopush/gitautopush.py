from subprocess import run, STDOUT
import os
import os.path as op
from time import sleep
import argparse
import shutil as sh

DESCRIPTION = (
    "Automatically syncronize and push a git repository to GitHub."
    "\n\n"
    "Useful for teaching with one of more files that you populate "
    "as you go along. This tool will automatically sync "
    "changes that you make and push them to GitHub so that "
    "students can use it as a reference."
)
parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument(
    "--path", default='.', help=("The path to the folder you'd like to watch. "
                                "Any changes to this folder will be committed and pushed.")
)
parser.add_argument(
    "--sleep", default=10, help="Time to wait (in seconds) before checking for updates."
)

NBVIEWER_BASE = "https://nbviewer.jupyter.org/github/{orgrepo}/blob/{branch}/{path}?flush_cache=true"
GITHUB_BASE = "https://github.com/{orgrepo}/blob/{branch}/{path}"


def main():
    # Parse args
    args = parser.parse_args()
    path = op.abspath(args.path)
    this_sleep = int(args.sleep)

    # Checks
    if not op.isdir(path):
        raise ValueError("Specified path does not exist: \n" + path)

    try:
        out = run("git rev-parse --abbrev-ref HEAD".split(), check=True,
                  capture_output=STDOUT, cwd=path)
        branch = out.stdout.decode().strip()

    except Exception:
        raise ValueError("A `git status` command didn't work, are you sure this is a git repository?")

    # Grab the URL of the remote
    out = run('git remote -v'.split(), capture_output=STDOUT, cwd=path)
    remotes = out.stdout.decode().strip().split('\n')
    remote = [ii for ii in remotes if '(push)' in ii][0].strip().split()[1]
    orgrepo = '/'.join(remote.split('/')[-2:])
    nbviewer_tree_link = NBVIEWER_BASE.format(
        orgrepo=orgrepo, branch=branch, path=''
    ).split('?')[0].replace('blob', 'tree')

    print('\n---')
    print("Observing changes to folder: " + op.abspath(path))
    print(f"Pushing changes to repository: {remote}/tree/{branch}")
    print("View notebooks at this nbviewer link: " + nbviewer_tree_link)

    # --- Main loop ---
    ii = 1
    while True:
        # Check for any changes in this folder
        out = run('git status --porcelain'.split(), capture_output=STDOUT, cwd=path)
        changed_files = out.stdout.decode().strip().split('\n')
        changed_files = [ii.strip().split(' ', 1)[-1] for ii in changed_files]
        changed_files = [ii for ii in changed_files if len(ii) > 0]

        # Remove some common files we don't want
        changed_files = [ii for ii in changed_files
                         if ".ipynb_checkpoints" not in ii]

        # Do nothing if we have no changed files
        if len(changed_files) == 0:
            continue

        # Check in all the changed files
        run("git add -A".split(), check=True, cwd=path)
        msg = "Updated files:\n\n"
        for ch_file in changed_files:
            tab = '    '
            if _is_ipynb(ch_file):
                nbviewer_extra = NBVIEWER_BASE.format(orgrepo=orgrepo, branch=branch, path=ch_file)
                nbviewer_extra = f"{nbviewer_extra}"
            else:
                nbviewer_extra = ''
            github_extra = GITHUB_BASE.format(orgrepo=orgrepo, branch=branch, path=ch_file)
            msg += f'{tab}{ch_file}\n{tab}{tab}{nbviewer_extra}\n{tab}{tab}{github_extra}\n'

        run(["git", "commit", "-m", f"gitautosync update {ii}"], check=True, capture_output=STDOUT, cwd=path)

        out = run(("git", "push"), capture_output=STDOUT, cwd=path)
        print("\n---\n")
        print(f"Update {ii}\n\n{msg}")
        ii += 1
        sleep(this_sleep)


def _is_ipynb(path):
    return op.splitext(path)[-1] == '.ipynb'

if __name__ == "__main__":
    main()
