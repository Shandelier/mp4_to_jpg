# A script that will take all .mp4 files from --input location
# and convert them to jpg files applying transformations like
# -croping
# -rescaling
# The output files will be stored in a folder "/pictures"
# under the --output path

import cv2
import os
import shutil
import argparse
from math import floor
from tqdm import tqdm
import pandas as pd
import numpy as np
import utils as ut

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str,
                    default=r"C:\Users\kluse\Documents\python\SSR-Dataset\test")
parser.add_argument('--output', type=str,
                    default=r"C:\Users\kluse\Documents\python\SSR-Dataset")
args = parser.parse_args()


def split_frame_file(file, out_path, downsampling=10):
    cap = cv2.VideoCapture(file)
    name = os.path.basename(file)
    out = out_path
    # posenet train picture size: 353x257
    dsize = (353, 257)

    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("{} vid of {} estimated frames".format(name, n_frames))

    i = 0
    while(True):
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, dsize)
            path = "{}/{}_{}.jpg".format(out, name, str(i))
            cv2.imwrite(path, frame)
            i += downsampling
            cap.set(1, i)
        else:
            break
    cap.release()
    n_samples = len(os.listdir(out))
    print("{} samples extracted".format(n_samples))


src_path = args.input + r"/"
files = ut.dir2files(src_path)
print("files found: ", files)

out_path = args.output + r"/pictures"
if not os.path.isdir(out_path):
    os.makedirs(out_path)

for file in files:
    split_frame_file(file, out_path, 1)

print("[  INFO  ] Extraction finished")
