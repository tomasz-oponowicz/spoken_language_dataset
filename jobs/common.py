import os
import shutil
import requests


def remove_extension(file):
    return os.path.splitext(file)[0]


def get_filename(file):
    return os.path.basename(remove_extension(file))


def get_dirname(file):
    return os.path.dirname(file)


def append_suffix_to_filename(file, suffix):
    root_and_ext = os.path.splitext(file)
    return root_and_ext[0] + suffix + root_and_ext[1]


def change_extension(file, new_extension):
    root_and_ext = os.path.splitext(file)
    return root_and_ext[0] + '.' + new_extension


def remove_file(file):
    os.remove(file)


def rename_file(src, dst):
    os.rename(src, dst)


def remove_directory(path):
    shutil.rmtree(path)


def create_directory(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def fetch(url, output_file):
    print("Downloading {0}".format(url))
    response = requests.get(url, stream=True)
    with open(output_file, 'wb') as file:
        shutil.copyfileobj(response.raw, file)
    del response
