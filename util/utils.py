import os
from datetime import datetime

def split_path(path):
    dir_ = os.path.dirname(path)
    filename = os.path.basename(path)
    file, ext = os.path.splitext(filename)
    return dir, file, ext

def get_now_time_str(flatten=False):
    now = datetime.now() # current date and time
    datetime_str = "%m/%d/%Y, %H:%M:%S" if not flatten else "%m_%d_%Y__%H_%M_%S"
    return now.strftime(datetime_str)

def read_file_lines(path):
    res = []
    with open(path, "r") as fp:
        for line in fp:
            res.append(line)
    return res
