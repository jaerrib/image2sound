import argparse

from sound_image import DEFAULT_SETTINGS, SoundImage

parser = argparse.ArgumentParser()
parser.add_argument(
    "-p", "--path", help="Path to the input image", default="test_image_rgb.png", type=str
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
    "-ts",
    "--time_signature",
    help="Sets the time signature as 3/4, 12/8, etc. Defaults to 4/4. The bottom number is handled as the number of notes per measure while the top determines how often to emphasize a note with a greater amplitude.",
    type=str,
)

parser.add_argument(
    "--method2",
    help="Whether to use the new conversion method",
    action="store_true",
)

parser.add_argument(
    "--smooth",
    help="Apply a smoothing filter",
    action="store_true",
)

parser.add_argument(
    "-adsr",
    "--adsr",
    help="Provide a general template for ADSR settings. Defaults to 'piano'. See envelope_settings.py for more options.",
    type=str,
)

parser.add_argument(
    "-w",
    "--waveform",
    help="Which waveform to use: sine, square, triangle, sawtooth or piano (which uses special harmonic generation) - defaults to sine",
    type=str,
)

data = vars(parser.parse_args())
data["overrides"] = []
for key in data:
    if data[key] is None:
        if data["reveal"]:
            data["overrides"].append(key)
        data[key] = DEFAULT_SETTINGS[key]
SoundImage(**{key: val for key, val in data.items() if val is not None}).convert()
