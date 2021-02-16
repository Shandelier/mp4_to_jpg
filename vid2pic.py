# A script that will take all .mp4 files from --input location
# and convert them to jpg files applying transformations like
# -croping
# -rescaling
# The output files will be stored in a folder "/pictures"
# under the --output path

import cv2
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--vid_dir', type=str,
                    default="./videos")
parser.add_argument('--output', type=str,
                    default="./output")
parser.add_argument('--downsampling', type=int,
                    default=1)
args = parser.parse_args()


def main():
    check_same_path()
    files = [
        f.path
        for f in os.scandir(args.vid_dir)
        if f.is_file() and f.path.endswith((".mp4"))
    ]
    print("files found: ", files)
    for file in files:
        vid_name = os.path.basename(file).split('.', 1)[0]
        output_dir = args.output + "/" + vid_name
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        split_frame_file(file, output_dir)
    print("[  INFO  ] Extraction finished")


def check_same_path():
    if args.vid_dir == args.output:
        print(
            "[WARNING] input dir is the same as output dir -- the pictures will be overwritten"
        )
        print("Do you wish to continue?: y/n")
        if input() != "y":
            exit()


def split_frame_file(file, out_dir):
    cap = cv2.VideoCapture(file)
    vid_name = os.path.basename(file).split('.', 1)[0]

    # posenet train picture size: 353x257
    # but video size is in 16:9 aspect ratio
    dsize = (320, 180)
    # TODO: cropping to native posenet size
    # cropsize = (353, 257)
    # crop_img = img[y:y+h, x:x+w]

    path = ""
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("{} vid of {} estimated frames (without downsampling)".format(
        os.path.basename(file), n_frames))

    progress_tenth = int(n_frames/(10*args.downsampling))
    current_progress = 0
    i = 0
    while(True):
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, dsize)
            path = "{}/{}.jpg".format(out_dir, str(i))
            cv2.imwrite(path, frame)
            i += args.downsampling
            current_progress += 1
            if (current_progress == progress_tenth):
                print("{}/% of video ready".format(int(i/n_frames*100)))
                current_progress = 0
            cap.set(1, i)
        else:
            break
    cap.release()
    n_samples = len(os.listdir(out_dir))
    print("[FINISH] {} samples extracted".format(n_samples))


if __name__ == "__main__":
    main()
