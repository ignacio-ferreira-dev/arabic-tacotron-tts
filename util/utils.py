import os

def split_path(path):
    dir_ = os.path.dirname(path)
    filename = os.path.basename(path)
    file, ext = os.path.splitext(filename)
    return dir, file, ext
