import argparse
from sound_image import SoundImage

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", default="test_image.png", type=str)
parser.add_argument("-key", "--key", default="C", type=str)
parser.add_argument("-t", "--tempo", default=60, type=int)
parser.add_argument("-min", "--minutes", default=1, type=int)
parser.add_argument("-sec", "--seconds", default=0, type=int)
parser.add_argument("--split", default=False, action="store_true")
args = parser.parse_args()

si = SoundImage(**{key: val for key, val in vars(args).items()
                   if val is not None})

si.convert()
