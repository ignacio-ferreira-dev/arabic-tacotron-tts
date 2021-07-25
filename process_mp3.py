import subprocess
import multiprocessing
import uuid
import argparse
import os
import shutil

from mp3_to_wav import convert_mp3_folder_to_wav

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Running pipeline with steps')
	parser.add_argument('--input_folder', "-f" ,type=str, required=True,help="folder with mp3 files")
	parser.add_argument('--csv', "-c" ,type=str , required=True,help="csv file")
	parser.add_argument('--out_folder', "-o" ,type=str, default = "training/custom_dataset" ,required=True,help="folder in which to save output processed files")

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
	shutil.copyfile(args.csv,os.path.join(temp_folder,"temp_filtered.csv"))
	
	subprocess.call("python mp3_to_wav.py --input_folder %s --out_folder %s" % (input_folder,wav_folder),shell=True)
	
	workers = multiprocessing.cpu_count()
	preprocess_cmd = "python preprocess.py --input_dir %s --output %s --dataset nawar --num_workers %d" % (temp_folder,out_folder,workers)
	print(preprocess_cmd)
	subprocess.call(preprocess_cmd, shell=True)

