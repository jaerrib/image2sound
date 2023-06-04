import argparse
from sound_image import SoundImage

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str)
parser.add_argument("-key", "--key", type=str)
parser.add_argument("-t", "--tempo", type=str)
parser.add_argument("-min", "--minutes", type=str)
parser.add_argument("-sec", "--seconds", type=str)
args = parser.parse_args()

kwargs = {
    "path": args.path,
    "key": args.key,
    "tempo": args.tempo,
    "minutes": args.minutes,
    "seconds": args.seconds,
}

si = SoundImage(**{key: val for key, val in kwargs.items() if val is not None})
si.convert_to_multiple()
