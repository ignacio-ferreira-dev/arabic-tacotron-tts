import argparse
import os
from synthesizer import Synthesizer
from util import audio, infolog, plot, ValueWindow
from util.utils import get_now_time_str, read_file_lines
import uuid
import time
import scipy

#Processes the input text and generates audio at out_folder
def generate_sound_from_text(input_text_path, model_path, out_folder):
    #Create folder
    os.makedirs(out_folder, exist_ok=True)
    #Load input text
    input_text = read_file_lines(input_text_path)
    #Initiate synthetizer
    synthesizer = Synthesizer()
    synthesizer.load(model_path)
    total_waveform = None
    for phrase in input_text:
        #Generate waveform
        waveform = synthesizer.synthesize(phrase, only_wav=True)
        if total_waveform is None:
            total_waveform = waveform
        else:
            total_waveform = scipy.vstack((total_waveform, waveform))
    #Save waveform
    out_file_path = os.path.join(out_folder, str(uuid.uuid4())+"__"+get_now_time_str(flatten=True)+".wav")
    audio.save_wav(total_waveform, out_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Running pipeline with steps')
    parser.add_argument('--input_text_path', "-i" ,type=str, required=True, help="input path to text to process")
    parser.add_argument('--model_path', "-m" ,type=str, required=True, help="path to model")
    parser.add_argument('--out_folder', "-o" ,type=str, default="output_predict" ,help="folder where to save output predictions")
    args = vars(parser.parse_args())
    input_text_path = args["input_text_path"]
    out_folder = args["out_folder"]
    model_path = args["model_path"]
    generate_sound_from_text(input_text_path, model_path, out_folder)
