import subprocess
import os
import shutil


def run_in_foreground(cmd):
    print(cmd)
    subprocess.check_call(cmd.split(), shell=False)


def remove_extension(file):
    return os.path.splitext(file)[0]


def get_filename(file):
    return os.path.basename(remove_extension(file))


def get_dirname(file):
    return os.path.dirname(file)


def append_suffix_to_filename(file, suffix):
    root_and_ext = os.path.splitext(file)
    return root_and_ext[0] + suffix + root_and_ext[1]


def remove_file(file):
    os.remove(file)


def remove_directory(path):
    shutil.rmtree(path)
