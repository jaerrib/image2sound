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
    default=DEFAULT_SETTINGS["output"],
    type=str,
)
parser.add_argument(
    "-key",
    "--key",
    help="Key of the output track as a capital letter, then a dash, plus"
    "Major/Minor/MajorPentatonic/MinorPentatonic/8Tone, without spaces",
    default=DEFAULT_SETTINGS["key"],
    type=str,
)
parser.add_argument(
    "-t",
    "--tempo",
    help="Tempo of the output track in beats per minute",
    default=DEFAULT_SETTINGS["tempo"],
    type=int,
)
parser.add_argument(
    "-min",
    "--minutes",
    help="Length of the output track in minutes",
    default=DEFAULT_SETTINGS["minutes"],
    type=int,
)
parser.add_argument(
    "-sec",
    "--seconds",
    help="Length of the output track in seconds",
    default=DEFAULT_SETTINGS["seconds"],
    type=int,
)
parser.add_argument(
    "--split",
    help="Whether to save the different subpixel tracks as separate files",
    default=DEFAULT_SETTINGS["split"],
    action="store_true",
)
parser.add_argument(
    "--reveal",
    help="Whether to use the image data itself to provide arguments",
    default=DEFAULT_SETTINGS["reveal"],
    action="store_true",
)

print(vars(parser.parse_args()))

SoundImage(
    **{key: val for key, val in vars(parser.parse_args()).items() if val is not None}
).convert()
