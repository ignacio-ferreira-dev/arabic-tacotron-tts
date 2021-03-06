import subprocess
import multiprocessing
import uuid
import argparse
import os
import shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Running pipeline with steps')
    parser.add_argument('--input_folder', "-f" ,type=str, required=True,help="folder with mp3 files")
    parser.add_argument('--csv', "-c" ,type=str , required=True,help="words CSV file to process")
    parser.add_argument('--out_folder', "-o" ,type=str, default = "training/custom_dataset" ,required=True,help="folder in which to save output processed files")
    parser.add_argument('--raw_csv', "-r" ,action="store_true",help="use this only when CSV file is already in processed format")
    parser.add_argument("--keep_temp","-k",action="store_true",help="Keep temporal wav folder")
    args = parser.parse_args()
    input_folder = args.input_folder
    out_folder = args.out_folder
    if not os.path.isdir(input_folder):
        print("Input folder doesn't exist.")
        exit(2)
    if not os.path.isfile(args.csv):
        print("CSV file doesn't exist.")
        exit(2)
    uuid_name = str(uuid.uuid4())
    temp_folder = "temp_" + uuid_name
    wav_folder = os.path.join(temp_folder,"wavs")
    os.makedirs(temp_folder,exist_ok=True)
    os.makedirs(wav_folder,exist_ok=True)
    os.makedirs(out_folder,exist_ok=True)
    print()
    print("MP3 conversion step:")
    convert_cmd = "python mp3_to_wav.py --input_folder %s --out_folder %s" % (input_folder,wav_folder)
    subprocess.call(convert_cmd,shell=True)
    
    # process words.csv step
    if args.raw_csv:
        shutil.copyfile(args.csv,os.path.join(temp_folder,"temp_filtered.csv"))
    else:
        words_cmd = "python process_words.py --input %s --output %s --wav %s" % (args.csv,os.path.join(temp_folder,"temp_filtered.csv"),wav_folder)
        subprocess.call(words_cmd, shell=True,stdout=subprocess.DEVNULL)

    print()
    print("Preprocessing step:")
    workers = multiprocessing.cpu_count()
    preprocess_cmd = "python preprocess.py --input_dir %s --output %s --dataset nawar --num_workers %d" % (temp_folder,out_folder,workers)
    subprocess.call(preprocess_cmd, shell=True)

    # delete temp files unless -k is passed
    if not args.keep_temp:
        contents = os.listdir(temp_folder)
        # ensure temp folder contains only autogenerated contents before deleting to be safe
        if ["temp_filtered.csv","wavs"] == sorted(contents):
            shutil.rmtree(temp_folder)
            print("Temp folder cleaned.")
        else:
            print("Temp folder was modified. Unable to delete.")

