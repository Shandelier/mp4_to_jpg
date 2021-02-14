import os
import re


def dir2files(path, extention="mp4"):
    return [
        path + x
        for x in os.listdir(path)
        if re.match("^([a-zA-Z0-9-_])+\.%s$" % extention, x)
    ]
