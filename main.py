import argparse
from sound_image import SoundImage

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str)
parser.add_argument("-key", "--key", type=str)
parser.add_argument("-t", "--tempo", type=str)
args = parser.parse_args()
path = args.path
key = args.key
tempo = args.tempo
si = SoundImage(path, key)
si.convert_to_multiple()

