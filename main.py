import argparse
from sound_image import SoundImage

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str)
parser.add_argument("-key", "--key", type=str)
parser.add_argument("-t", "--tempo", type=str)
args = parser.parse_args()

kwargs = {
    "path": args.path,
    "key": args.key,
    "tempo": args.tempo,
}

si = SoundImage(**{key: val for key, val in kwargs.items() if val is not None})
si.convert_to_multiple()
