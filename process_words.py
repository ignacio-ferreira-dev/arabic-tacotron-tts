import csv 
import argparse
import os
import csv

parser = argparse.ArgumentParser(description='CSV format')
parser.add_argument('--input', "-f" ,type=str, required=True, help="input csv file")
parser.add_argument('--output', "-o" ,type=str, required=True, help="output csv file for preprocess.py")
parser.add_argument("--filename_column","-n",type=str,default='2',help="name of filename column")
parser.add_argument("--text_column","-t",type=str,default='0',help="name of arabic text column")
parser.add_argument("--wav","-w",type=str,default='0',required=True,help="wav folder")
args = parser.parse_args()

with open(args.input) as csvfile:
    with open(args.output,"w") as outfile:
        reader = csv.DictReader(csvfile,delimiter=",")
        writer = csv.writer(outfile,delimiter="|",quoting=csv.QUOTE_NONE)
        for row in reader:
            fname = row[args.filename_column]
            text = row[args.text_column]
            numbers = tuple([int(n,base=10) for n in fname.split("_")])
            fixed_fname = "%03d_%03d_%03d" % numbers
            #if fname != fixed_fname:
            #    print(fname,"->",fixed_fname)
            wav_name = os.path.join(args.wav,fixed_fname+".wav")
            if not os.path.isfile(wav_name):
                print(wav_name,"not found!")
            else:
                writer.writerow([fixed_fname,text])
        
