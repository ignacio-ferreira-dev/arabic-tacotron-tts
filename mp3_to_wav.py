import argparse
from os import path
import os

from util.utils import split_path
from tqdm import tqdm
import glob
import subprocess
import multiprocessing

# take argument as a tuple so it can be called easily by imap 
def convert_file_job(args):
    filename,out_folder,overwrite = args
    dir, file, ext = split_path(filename)

    out_path = path.join(out_folder, file+".wav")
    assert filename != out_path
    if overwrite or not path.exists(out_path):
        code = mp3_to_wav(filename, out_path,overwrite=overwrite)
        return code,out_path
    else:
        return ("E",out_path)
    

#Iterate over folder and convert files from mp3 to wav
def convert_mp3_folder_to_wav(in_folder, out_folder,recursive=True,mp=True,overwrite=False):
    #Process all mp3 files
    mp3_files = glob.glob(path.join(glob.escape(in_folder),"**/*.mp3"),recursive=recursive)
    
    # adding wav files to the processing queue won't cause any issue with ffmpeg
    wav_files = glob.glob(path.join(glob.escape(in_folder),"**/*.wav"),recursive=recursive)
    mp3_files = mp3_files + wav_files
    
    pbar = tqdm(total=len(mp3_files))
    errors = []
    existing = []
    ok = []
    
    # optionally run multiple process to increase file handling and decoding speed (3 are enough, too many will hang the terminal)
    cpu_count = max(3,multiprocessing.cpu_count()) if mp else 1
    with multiprocessing.Pool(processes=cpu_count) as pool:
        for code,out_name in pool.imap_unordered(convert_file_job,[(input_file,out_folder,overwrite) for input_file in mp3_files]):
            if code == "E":
                # This case is handled separately
                existing.append(out_name)
            elif code > 1:
                # 0 means OK, 1 means warning, >= 2 means error
                errors.append(out_name)
            else:
                ok.append(out_name)
            pbar.update(1)
    # check that all output names are unique (it should never fail)
    assert len(ok) == len(set(ok))
    if len(existing) > 0:
        print("[WARNING] The following",len(existing),"files already exist:")
        for f in sorted(existing[:20]):
            print(f)
        if len(existing) > 20:
            print("...")
    if len(errors) > 0:
        print("[ERROR] The following",len(existing),"files could not be converted:")
        for f in sorted(errors):
            print(f)
    print(len(ok),"files converted succesfully.") 
    pbar.close()
    # fix console if it's stuck
    try:
        subprocess.call("stty sane",shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    except:
        pass

# convert wav to mp3
def mp3_to_wav(in_file, out_file,overwrite=False):
    #sound = AudioSegment.from_mp3(in_file) # from pydub
    #sound.export(out_file, format="wav")
    overwrite_option = "-y" if overwrite else "-n"
    program = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"
    return_code = subprocess.call(" ".join([program,overwrite_option,'-nostdin -i',in_file,out_file]),shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    return return_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Running pipeline with steps')
    parser.add_argument('--input_folder', "-f" ,type=str, default = "custom_datasets/20", help="folder with mp3 files")
    parser.add_argument('--out_folder', "-o" ,type=str, default = "custom_datasets/output" ,help="folder in which to save output wav files")
    args = vars(parser.parse_args())
    input_folder = args["input_folder"]
    out_folder = args["out_folder"]
    os.makedirs(out_folder, exist_ok=True)
    convert_mp3_folder_to_wav(input_folder, out_folder)
