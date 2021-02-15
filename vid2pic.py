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
parser.add_argument('--downsampling', type=int,
                    default=1)
args = parser.parse_args()


def split_frame_file(file, out_path, downsampling=10):
    cap = cv2.VideoCapture(file)
    out = out_path

    # posenet train picture size: 353x257
    # but video size is in 16:9 aspect ratio
    dsize = (457, 257)
    # TODO: cropping
    # cropsize = (353, 257)
    # crop_img = img[y:y+h, x:x+w]

    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("{} vid of {} estimated frames".format(
        os.path.basename(file), n_frames))

    i = 0
    while(True):
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, dsize)
            path = "{}/{}_{}.jpg".format(out,
                                         os.path.splitext(file)[0], str(i))
            cv2.imwrite(path, frame)
            i += downsampling
            if not i % (n_frames/10):
                print("{}/% of video ready".format(i/n_frames*100))
            cap.set(1, i)
        else:
            break
    cap.release()
    n_samples = len(os.listdir(out))
    print("{} samples extracted".format(n_samples))


downsampling = args.downsampling

src_path = args.input + r"/"
files = ut.dir2files(src_path)
print("files found: ", files)

out_path = args.output + r"/pictures"
if not os.path.isdir(out_path):
    os.makedirs(out_path)

for file in files:
    split_frame_file(file, out_path, downsampling)

print("[  INFO  ] Extraction finished")
