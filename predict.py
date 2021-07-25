import argparse
import os
from synthesizer import Synthesizer
from util import audio, infolog, plot, ValueWindow
from util.utils import get_now_time_str, read_file_lines,split_path
import uuid
import time
import scipy
import glob
import tensorflow as tf

#Processes the input text and generates audio at out_folder
def generate_sound_from_text(input_text_paths, model_path, out_folder):
    #Create folder
    os.makedirs(out_folder, exist_ok=True)
    #Initiate synthetizer
    synthesizer = Synthesizer()
    synthesizer.load(model_path)
    for input_text_path in input_text_paths:
        #Load input text
        input_text = read_file_lines(input_text_path)
        total_waveform = None
        for phrase in input_text:
            #Generate waveform
            waveform = synthesizer.synthesize(phrase, only_wav=True)
            if total_waveform is None:
                total_waveform = waveform
            else:
                total_waveform = scipy.vstack((total_waveform, waveform))
        #Save waveform
        _, input_fname, _ = split_path(input_text_path)
        uuid_name = str(uuid.uuid4())
        out_file_path = os.path.join(out_folder, input_fname.split(".")[0]  +"__"+get_now_time_str(flatten=True)+".wav")
        audio.save_wav(total_waveform, out_file_path)

def find_txt_files(folder):
    txt_files = glob.glob(os.path.join(folder,'./*.txt'))
    return txt_files

if __name__ == "__main__":
    try:
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.FATAL) # remove unnecesary output to console
        from tensorflow.python.util import deprecation
        deprecation._PRINT_DEPRECATION_WARNINGS = False
    except:
        pass
    parser = argparse.ArgumentParser(description='Running pipeline with steps')
    parser.add_argument('--input_text_path', "-i" ,type=str, required=True, help="input path to text file or folder containing *.txt files to process")
    parser.add_argument('--model_path', "-m" ,type=str, required=True, help="path to model")
    parser.add_argument('--out_folder', "-o" ,type=str, default="output_predict" ,help="folder where to save output predictions")
    args = vars(parser.parse_args())
    if os.path.isdir(args["input_text_path"]):
        input_text_paths = find_txt_files(args["input_text_path"])
    else:
         input_text_paths = [args["input_text_path"]]
    out_folder = args["out_folder"]
    model_path = args["model_path"]
    generate_sound_from_text(input_text_paths, model_path, out_folder)
