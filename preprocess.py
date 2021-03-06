import argparse
import os
from multiprocessing import cpu_count
from tqdm import tqdm
from datasets import  nawar
from hparams import hparams


def preprocess_nawar(args):
  in_dir = args.input_dir
  out_dir = args.output
  os.makedirs(out_dir, exist_ok=True)
  metadata = nawar.build_from_path(in_dir, out_dir, args.num_workers, tqdm=tqdm)
  write_metadata(metadata, out_dir)

def write_metadata(metadata, out_dir):
  with open(os.path.join(out_dir, 'train.txt'), 'w', encoding='utf-8') as f:
    for m in metadata:
      f.write('|'.join([str(x) for x in m]) + '\n')
  frames = sum([m[2] for m in metadata])
  hours = frames * hparams.frame_shift_ms / (3600 * 1000)
  print('Wrote %d utterances, %d frames (%.2f hours)' % (len(metadata), frames, hours))
  print('Max input length:  %d' % max(len(m[3]) for m in metadata))
  print('Max output length: %d' % max(m[2] for m in metadata))


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_dir', type=str, required=True)
  parser.add_argument('--output', type=str, required=True)
  parser.add_argument('--dataset', required=True, default="nawar", choices=['nawar'])
  parser.add_argument('--num_workers', type=int, default=cpu_count())
  args = parser.parse_args()
  if args.dataset == 'nawar':
    preprocess_nawar(args)


if __name__ == "__main__":
  main()
