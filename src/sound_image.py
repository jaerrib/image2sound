import math
import os

import numpy as np
import wavio
from PIL import Image

import dimension_calc
import tone_array

RATE = 44100


class SoundImage:
    def __init__(self, path, output, key, tempo, minutes, seconds, split, reveal):
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

    def open_file(self):
        return Image.open(self.path).convert(mode="RGB")

    def image_to_array(self, img):
        self.image_array = np.asarray(
            img.resize(dimension_calc.get_new_dim(img.size, self.minutes, self.tempo)),
            dtype="int64",
        )
        return self

    def get_freq(self, color):
        return self.freq_dict[int(math.trunc(color / (256 / self.length)))]

    def get_sin(self, color):
        return np.sin(
            2
            * np.pi
            * self.get_freq(color)
            * np.arange(int(RATE * 60 / self.tempo))
            / RATE
        )

    @staticmethod
    def save_wav(input_path, output_path, side, array):
        file_name = ".".join(input_path.split(".")[:-1]).split("/")[-1] + side + ".wav"
        if output_path == "":
            pass
        elif os.path.isdir(output_path):
            file_name = output_path + file_name
        else:
            file_name = output_path
        wavio.write(file_name, array, RATE, scale=2, sampwidth=3, clip="ignore")
        print("Saved file as " + file_name)

    def convert_to_multiple(self):
        red_array, green_array, blue_array = [], [], []
        for x in self.image_array:
            for y in x:
                red_array.append(self.get_sin(y[0]))
                green_array.append(self.get_sin(y[1]))
                blue_array.append(self.get_sin(y[2]))
        self.save_wav(self.path, self.output, "-R", red_array)
        self.save_wav(self.path, self.output, "-G", green_array)
        self.save_wav(self.path, self.output, "-B", blue_array)

    def convert_to_stereo(self):
        left_data, right_data = [], []
        for x in self.image_array:
            for y in x:
                left_data.append(self.get_sin((y[0] + y[1]) / 2))
                right_data.append(self.get_sin((y[2] + y[1]) / 2))
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
        if self.split:
            self.convert_to_multiple()
        else:
            self.convert_to_stereo()

    @staticmethod
    def determine_key(self, red, green, blue):
        notes = tone_array.get_chromatic_notes()
        key = notes[math.trunc(red / (len(notes)))] + (
            "Major" if blue % 2 == 0 else "Minor"
        )
        if green % 2 == 0:
            key += "Pentatonic"
        self.key = key
        return self

    def override(self, img):
        tiny_img_arr = np.asarray(img.resize((1, 1)), dtype="int64")
        red = tiny_img_arr[0][0][0]
        green = tiny_img_arr[0][0][1]
        blue = tiny_img_arr[0][0][2]
        self.tempo = (red + green + blue) / 3
        self.determine_key(self, red=red, green=green, blue=blue)
        self.minutes = math.sqrt((img.size[0] + img.size[1]) / 2) / 2
        return self
