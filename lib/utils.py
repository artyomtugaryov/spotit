import os
from os import listdir
from os.path import isfile


def list_files_in_dir(directory):
    return [f for f in listdir(directory) if isfile(os.path.join(directory, f))]
