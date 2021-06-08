import argparse
import pydub
from os import path
import os
from pydub import AudioSegment
from util.utils import split_path
from tqdm import tqdm

#Iterate over folder and convert files from mp3 to wav
def convert_mp3_folder_to_wav(in_folder, out_folder):
    #Process all mp3 files
    files = [elem for elem in os.listdir(in_folder) if elem.endswith(".mp3")]
    pbar = tqdm(total=len(files))
    for filename in files:
        in_path = path.join(in_folder, filename)
        dir, file, ext = split_path(filename)
        #If file is not mp3 continue
        out_path = path.join(out_folder, file+".wav")
        mp3_to_wav(in_path, out_path)
        pbar.update(1)
    pbar.close()

# convert wav to mp3
def mp3_to_wav(in_file, out_file):
    sound = AudioSegment.from_mp3(in_file)
    sound.export(out_file, format="wav")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Running pipeline with steps')
    parser.add_argument('--input_folder', "-f" ,type=str, default = "custom_datasets/20", help="folder with mp3 files")
    parser.add_argument('--out_folder', "-o" ,type=str, default = "custom_datasets/output" ,help="folder in which to save output wav files")
    args = vars(parser.parse_args())
    input_folder = args["input_folder"]
    out_folder = args["out_folder"]
    os.makedirs(out_folder, exist_ok=True)
    convert_mp3_folder_to_wav(input_folder, out_folder)
