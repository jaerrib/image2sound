import argparse
from sound_image import SoundImage

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="Path to the input image", type=str)
parser.add_argument("-key", "--key", help="Key of the output track as a capital letter", type=str)
parser.add_argument("-t", "--tempo", help="Tempo of the output track in beats per minute", type=str)
parser.add_argument("-min", "--minutes", help="Length of the output track in minutes", type=str)
parser.add_argument("-sec", "--seconds", help="Length of the output track in seconds", type=str)
parser.add_argument("--split", help="Whether to save the different subpixel tracks as separate files", action="store_true")
args = parser.parse_args()

si = SoundImage(**{key: val for key, val in vars(args).items()
                   if val is not None})

si.convert()
