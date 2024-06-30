import math
import os

import numpy as np
import wavio
from PIL import Image
from halo import Halo
from mutagen.id3 import APIC
from mutagen.wave import WAVE

import dimension_calc
import tone_array

RATE = 44100
DEFAULT_SETTINGS = {
    "path": "test_image.png",
    "output": "",
    "key": "C-Major",
    "tempo": 60,
    "minutes": 1,
    "seconds": 0,
    "split": False,
    "reveal": False,
    "method2": False,
}


class SoundImage:
    def __init__(
        self,
        path,
        output,
        key,
        tempo,
        minutes,
        seconds,
        split,
        reveal,
        method2,
        overrides,
    ):
        self.path = path
        self.output = output
        self.key = key
        self.freq_dict = tone_array.get_tone_array(self.key)
        self.length = len(self.freq_dict)
        self.tempo = tempo
        self.minutes = minutes + seconds / 60
        self.image_array = None
        self.split = split
        self.reveal = reveal
        self.overrides = overrides
        self.method2 = method2

    def open_file(self):
        return Image.open(self.path).convert(mode="RGB")

    def image_to_array(self, img):
        self.image_array = np.asarray(
            img.resize(dimension_calc.get_new_dim(img.size, self.minutes, self.tempo)),
            dtype="int64",
        )
        return self

    def get_freq(self, color, freq_range):
        return freq_range[math.trunc(color / (256 / len(freq_range))) - 1]

    def get_sin(self, color, freq_range):
        amplitude = 1
        duration = 60 / self.tempo
        freq = self.get_freq(color, freq_range)

        sine_wave = amplitude * (
            np.sin(2 * np.pi * np.arange(RATE * duration) * freq / RATE)
        ).astype(np.float32)

        # Apply the Blackman window to remove clickiness cause by partial waveforms
        blackman_window = np.blackman(len(sine_wave))
        sine_wave *= blackman_window

        return sine_wave

    @staticmethod
    def save_wav(input_path, output_path, side, array):
        file_name = ".".join(input_path.split(".")[:-1]).split("/")[-1] + side + ".wav"
        if output_path == "":
            pass
        elif os.path.isdir(output_path):
            file_name = output_path + file_name
        else:
            file_name = output_path
        with Halo(text="Saving file…", color="white"):
            wavio.write(file_name, array, RATE, scale=2, sampwidth=3, clip="ignore")
            audio_file = WAVE(file_name)
            audio_file.add_tags()
            audio_file.tags.add(
                APIC(
                    encoding=3,  # 3 is for utf-8
                    mime=f"image/{Image.open(input_path).format.lower()}",  # can be image/jpeg or image/png
                    type=3,  # 3 is for the cover image
                    desc="Cover",
                    data=open(input_path, mode="rb").read(),
                )
            )
            audio_file.save()
        print("Saved file as " + file_name)

    def convert_to_multiple(self):
        with Halo(text="Converting data…", color="white"):
            red_array, green_array, blue_array = [], [], []
            for x in self.image_array:
                for y in x:
                    red_array.append(self.get_sin(y[0], self.freq_dict))
                    green_array.append(self.get_sin(y[1], self.freq_dict))
                    blue_array.append(self.get_sin(y[2], self.freq_dict))
        self.save_wav(
            self.path,
            self.output,
            "-R",
            np.hstack((np.array(red_array).reshape(-1, 1),)),
        )
        self.save_wav(
            self.path,
            self.output,
            "-G",
            np.hstack((np.array(green_array).reshape(-1, 1),)),
        )
        self.save_wav(
            self.path,
            self.output,
            "-B",
            np.hstack((np.array(blue_array).reshape(-1, 1),)),
        )

    def convert_to_stereo(self):
        with Halo(text="Converting data…", color="white"):
            left_data, right_data = [], []
            for x in self.image_array:
                for y in x:
                    left_data.append(self.get_sin((y[0] + y[1]) / 2, self.freq_dict))
                    right_data.append(self.get_sin((y[2] + y[1]) / 2, self.freq_dict))
        self.save_wav(
            self.path,
            self.output,
            "-stereo",
            np.hstack(
                (
                    np.array(left_data).reshape(-1, 1),
                    np.array(right_data).reshape(-1, 1),
                )
            ),
        )

    def convert(self):
        img = self.open_file()
        if self.reveal:
            self.override(img)
        self.image_to_array(img)
        if self.method2:
            self.convert_to_stereo_with_new_method()
        elif self.split:
            self.convert_to_multiple()
        else:
            self.convert_to_stereo()

    def determine_key(self, red, green, blue):
        notes = tone_array.get_chromatic_notes()
        key = notes[math.trunc(red / (255 / len(notes)))] + (
            "Major" if blue % 2 == 0 else "Minor"
        )
        if type(math.sqrt(red * green * blue)) is not float:
            key = notes[math.trunc(red / (255 / len(notes)))] + "8Tone"
        elif green % 16 == 0:
            key += "Pentatonic"
        self.key = key
        return self

    def override(self, img):
        tiny_img_arr = np.asarray(img.resize((1, 1)), dtype="int64")
        red = tiny_img_arr[0][0][0]
        green = tiny_img_arr[0][0][1]
        blue = tiny_img_arr[0][0][2]
        if "tempo" in self.overrides:
            self.tempo = (red + green + blue) / 3
        if "key" in self.overrides:
            self.determine_key(red=red, green=green, blue=blue)
        if "minutes" in self.overrides and "seconds" in self.overrides:
            self.minutes = math.sqrt((img.size[0] + img.size[1]) / 2) / 2
        return self

    def convert_to_stereo_with_new_method(self):
        left_freq_range = []
        right_freq_range = []
        for num in self.freq_dict:
            if num <= tone_array.FREQ_DICT["C5"]:
                left_freq_range.append(num)
            elif tone_array.FREQ_DICT["C4"] <= num <= tone_array.FREQ_DICT["C7"]:
                right_freq_range.append(num)
        with Halo(text="Converting data…", color="white"):
            left_data, right_data = [], []
            for x in self.image_array:
                for y in x:
                    left_data.append(self.get_sin((y[0] + y[1]) / 2, left_freq_range))
                    right_data.append(self.get_sin((y[2] + y[1]) / 2, right_freq_range))
        self.save_wav(
            self.path,
            self.output,
            "-stereo",
            np.hstack(
                (
                    np.array(left_data).reshape(-1, 1),
                    np.array(right_data).reshape(-1, 1),
                )
            ),
        )
