"""
Author       : zhangxianbing
Date         : 2021-05-27 15:20:49
Description  : 
LastEditors  : zhangxianbing
LastEditTime : 2021-05-27 20:53:30
"""
import os
import shutil


def read_requirements():
    reqs = []
    with open("requirements.txt", "r") as f:
        for line in f:
            reqs.append(line.strip())

    return reqs


def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
    return long_description


# If python>=3.8, you could use shutil.copytree(src, dst, dirs_exist_ok=False)
def copytree(src, dst, symlinks=False, ignore=None):
    """copytree that enables dirs_exist_ok. If python>=3.8, you could use shutil.copytree(src, dst, dirs_exist_ok=False)

    Args:
        src ([type]): src dir
        dst ([type]): dst dir
        symlinks (bool, optional): [description]. Defaults to False.
        ignore ([type], optional): [description]. Defaults to None.
    """
    print(f"Installing {src} to {dst}...")
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                copytree(s, d, symlinks, ignore)
            else:
                shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def find_line(filepat, pattern):
    with open(filepat, "r") as f:
        for l in f:
            if l.strip() == pattern:
                return True
    return False


def enable_complete(prog_name):
    bashrc_path = os.path.expanduser("~/.bashrc")
    line = f'eval "$(register-python-argcomplete {prog_name})"'
    added_lines = f"# {prog_name} (added by pyclier)\n{line}\n"

    if find_line(bashrc_path, line):
        print(f"Already added the following lines to: {bashrc_path}\n{added_lines}")
        return

    print(f"The following lines already exists in {bashrc_path}:\n{added_lines}")

    with open(bashrc_path, "a") as f:
        f.write(added_lines)
