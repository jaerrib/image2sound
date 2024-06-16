import argparse

from sound_image import DEFAULT_SETTINGS, SoundImage

parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--path", help="Path to the input image", default="test_image.png", type=str
)
parser.add_argument(
    "-o",
    "--output",
    help="The filepath to save the output file to",
    type=str,
)
parser.add_argument(
    "-key",
    "--key",
    help="Key of the output track as a capital letter, then a dash, plus"
    "Major/Minor/MajorPentatonic/MinorPentatonic/8Tone, without spaces",
    type=str,
)
parser.add_argument(
    "-t",
    "--tempo",
    help="Tempo of the output track in beats per minute",
    type=int,
)
parser.add_argument(
    "-min",
    "--minutes",
    help="Length of the output track in minutes",
    type=int,
)
parser.add_argument(
    "-sec",
    "--seconds",
    help="Length of the output track in seconds",
    type=int,
)
parser.add_argument(
    "--split",
    help="Whether to save the different subpixel tracks as separate files",
    action="store_true",
)
parser.add_argument(
    "--reveal",
    help="Whether to use the image data itself to provide arguments",
    action="store_true",
)

parser.add_argument(
    "--method2",
    help="Whether to use the new conversion method",
    action="store_true",
)


data = vars(parser.parse_args())
data["overrides"] = []
for key in data:
    if data[key] is None:
        if data["reveal"]:
            data["overrides"].append(key)
        data[key] = DEFAULT_SETTINGS[key]
SoundImage(**{key: val for key, val in data.items() if val is not None}).convert()
