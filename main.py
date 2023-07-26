import argparse
from sound_image import SoundImage

parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--path",
    help="Path to the input image",
    default="test_image.png",
    type=str)
parser.add_argument(
    "-key",
    "--key",
    help="Key of the output track as a capital letter plus"
         "Major/Minor, without spaces",
    default="CMajor",
    type=str)
parser.add_argument(
    "-t", "--tempo",
    help="Tempo of the output track in beats per minute",
    default=60,
    type=int)
parser.add_argument(
    "-min", "--minutes",
    help="Length of the output track in minutes",
    default=1,
    type=int)
parser.add_argument(
    "-sec", "--seconds",
    help="Length of the output track in seconds",
    default=0,
    type=int)
parser.add_argument(
    "--split",
    help="Whether to save the different subpixel tracks as separate files",
    default=False,
    action="store_true")
parser.add_argument(
    "--reveal",
    help="Whether to use the image data itself to provide arguments",
    default=False,
    action="store_true")
args = parser.parse_args()

si = SoundImage(**{key: val for key, val in vars(args).items()
                   if val is not None})

si.convert()
