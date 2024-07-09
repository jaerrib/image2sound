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
    "split": True,
    "reveal": False,
    "method2": False,
    "nosmooth": False,
    "time_signature": "1/1",
    "quartet": False,
}


class QuartetImage:
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
        nosmooth,
        time_signature,
        quartet,
    ):
        self.path = path
        self.output = output
        self.key = key
        self.freq_dict = tone_array.get_tone_array(self.key)
        self.length = len(self.freq_dict)
        self.time_signature = self.separate_time_signature(time_signature)
        self.tempo = tempo
        self.note_length = self.get_note_length()
        self.minutes = minutes + seconds / 60
        self.image_array = None
        self.split = split
        self.reveal = reveal
        self.overrides = overrides
        self.method2 = method2
        self.nosmooth = nosmooth
        self.quartet = quartet

    def open_file(self):
        with Image.open(self.path) as im:
            im = im.convert("CMYK")
        return im

    def image_to_array(self, img):
        self.image_array = np.asarray(
            img.resize(
                dimension_calc.get_new_dim(
                    img.size, self.minutes, self.tempo, self.time_signature
                )
            ),
            dtype="int64",
        )
        return self

    def get_note_length(self):
        duration = 60 / self.tempo
        note_length = duration / self.time_signature[1]
        return note_length

    def separate_time_signature(self, time_signature):
        top, bottom = time_signature.split("/")
        top, bottom = int(top), int(bottom)
        if top == 0:
            top = 1
        if bottom == 0:
            bottom = 1
        split_time_signature = [top, bottom]
        return split_time_signature

    @staticmethod
    def get_freq(color, freq_range):
        return freq_range[math.trunc(color / (256 / len(freq_range))) - 1]

    def get_sin(self, color, freq_range, amplitude):
        freq = self.get_freq(color, freq_range)
        sine_wave = amplitude * (
            np.sin(2 * np.pi * np.arange(RATE * self.note_length) * freq / RATE)
        ).astype(np.float32)
        if not self.nosmooth:
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
            file_name = file_name
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

    def get_amplitude(self, index):
        # Accents the first beat of each measure by applying a higher amplitude
        if index % self.time_signature[0] == 0:
            return 1
        return 0.5

    def create_quartet(self):
        cyan_freq_range = []
        magenta_freq_range = []
        yellow_freq_range = []
        black_freq_range = []
        for num in self.freq_dict:
            if tone_array.FREQ_DICT["G3"] <= num <= tone_array.FREQ_DICT["A7"]:
                cyan_freq_range.append(num)
            if tone_array.FREQ_DICT["C3"] <= num <= tone_array.FREQ_DICT["C7"]:
                magenta_freq_range.append(num)
            if tone_array.FREQ_DICT["C2"] <= num <= tone_array.FREQ_DICT["C6"]:
                yellow_freq_range.append(num)
            if tone_array.FREQ_DICT["C1"] <= num <= tone_array.FREQ_DICT["C5"]:
                black_freq_range.append(num)
        with Halo(text="Converting data…", color="white"):
            cyan_array, magenta_array, yellow_array, black_array = [], [], [], []
            index = 0
            for x in self.image_array:
                for y in x:
                    amplitude = self.get_amplitude(index)
                    cyan_array.append(self.get_sin(y[0], cyan_freq_range, amplitude))
                    magenta_array.append(self.get_sin(y[1], magenta_freq_range, amplitude))
                    yellow_array.append(self.get_sin(y[2], yellow_freq_range, amplitude))
                    black_array.append(self.get_sin(y[3], black_freq_range, amplitude))
                    index += 1
        self.save_wav(
            self.path,
            self.output,
            "-C",
            np.hstack((np.array(cyan_array).reshape(-1, 1),)),
        )
        self.save_wav(
            self.path,
            self.output,
            "-M",
            np.hstack((np.array(magenta_array).reshape(-1, 1),)),
        )
        self.save_wav(
            self.path,
            self.output,
            "-Y",
            np.hstack((np.array(yellow_array).reshape(-1, 1),)),
        )
        self.save_wav(
            self.path,
            self.output,
            "-K",
            np.hstack((np.array(black_array).reshape(-1, 1),)),
        )


    def convert(self):
        img = self.open_file()
        self.image_to_array(img)
        self.create_quartet()
