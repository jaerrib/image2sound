import argparse

from envelope_settings import envelope_settings
from movement_definitions import movement_type
from sound_image import DEFAULT_SETTINGS, SoundImage
from tone_array import SCALE_PATTERNS

parser = argparse.ArgumentParser()
parser.add_argument(
    "-p",
    "--path",
    help="Path to the input image",
    default="test_image_rgb.png",
    type=str,
)
parser.add_argument(
    "-o",
    "--output",
    help="The filepath to save the output file to",
    type=str,
)
available_scale_patterns = ", ".join(SCALE_PATTERNS.keys())
parser.add_argument(
    "-key",
    "--key",
    help="Key of the output track as a capital letter, then a dash, plus "
    f"one of  {available_scale_patterns}, without spaces. For example: C-Major.",
    type=str,
)
parser.add_argument(
    "-t",
    "--tempo",
    help="Tempo of the output track in beats per minute",
    type=int,
)
parser.add_argument(
    "--reveal",
    help="Whether to use the image data itself to provide arguments",
    action="store_true",
)
parser.add_argument(
    "-ts",
    "--time_signature",
    help="Sets the time signature as 3/4, 12/8, etc. Defaults to 4/4. When "
    "converting to WAV format, the bottom number is handled as the number of "
    "notes per measure while the top determines how often to emphasize a note "
    "with a greater amplitude. In midi conversion, the time signature is handled correctly.",
    type=str,
)
parser.add_argument(
    "--method2",
    help="Whether to use an alternate conversion method, splitting audio into frequency ranges associated with 'left-hand' and 'right-hand' piano parts.",
    action="store_true",
)
parser.add_argument(
    "--smooth",
    help="Apply a smoothing filter",
    action="store_true",
)
available_envelopes = ", ".join(envelope_settings.keys())
parser.add_argument(
    "-adsr",
    "--adsr",
    help=f"Provide a general template for ADSR settings. Defaults to 'piano'.  Available types: {available_envelopes}.",
    type=str,
)

parser.add_argument(
    "-w",
    "--waveform",
    help="Which waveform to use: sine, square, triangle, sawtooth or piano (which uses special harmonic generation) - defaults to sine",
    type=str,
)
parser.add_argument(
    "--midi",
    help="Whether to convert to MIDI instead of WAV",
    action="store_true",
)
available_types = ", ".join(movement_type.keys())
parser.add_argument(
    "-mt",
    "--movement_type",
    help=f"Provide a movement type template to the composition engine when using midi output. Defaults to 'sonata'. Available types: {available_types}",
    type=str,
)


data = vars(parser.parse_args())
data["overrides"] = []
for key in data:
    if data[key] is None:
        if data["reveal"]:
            data["overrides"].append(key)
        data[key] = DEFAULT_SETTINGS[key]

new_sound_image: SoundImage = SoundImage(data)
new_sound_image.convert()
