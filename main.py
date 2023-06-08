import argparse
from sound_image import SoundImage

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str)
parser.add_argument("-key", "--key", type=str)
parser.add_argument("-t", "--tempo", type=str)
parser.add_argument("-min", "--minutes", type=str)
parser.add_argument("-sec", "--seconds", type=str)
args = parser.parse_args()

si = SoundImage(**{key: val for key, val in vars(args).items()
                   if val is not None})

# si.convert_to_multiple()
si.convert_to_stereo()
