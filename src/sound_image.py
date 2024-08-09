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
    "nosmooth": False,
    "time_signature": "1/1",
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
        nosmooth,
        time_signature,
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
        self.image_mode = None

    def open_file(self):
        return Image.open(self.path)

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

    @staticmethod
    def apply_blackman(wave):
        # Apply the Blackman window to remove clickiness cause by partial waveforms
        blackman_window = np.blackman(len(wave))
        wave *= blackman_window
        return wave

    def get_wave(self, color, freq_range, amplitude, wave_type):
        freq = self.get_freq(color, freq_range)
        t = np.linspace(
            0, self.note_length, int(RATE * self.note_length), endpoint=False
        )
        match wave_type:
            case "sine":
                wave = amplitude * (np.sin(2 * np.pi * t * freq))
            case "square":
                wave = amplitude * 0.5 * (1 + np.sign(np.sin(2 * np.pi * freq * t)))
            case "triangle":
                wave = amplitude * (
                    2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
                )
            case "sawtooth":
                wave = amplitude * 2 * (t * freq - np.floor(0.5 + t * freq))
            case _:
                wave = amplitude * (np.sin(2 * np.pi * t * freq))
        if not self.nosmooth:
            wave = self.apply_blackman(wave)
        return wave

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

    def convert_to_multiple(self):
        with Halo(text="Converting data…", color="white"):
            for char in self.image_mode:
                if self.method2:
                    freq_range = []
                    for num in self.freq_dict:
                        if char == "R":
                            if num <= tone_array.FREQ_DICT["C5"]:
                                freq_range.append(num)
                        else:
                            if (
                                tone_array.FREQ_DICT["C4"]
                                <= num
                                <= tone_array.FREQ_DICT["C7"]
                            ):
                                freq_range.append(num)
                else:
                    freq_range = self.freq_dict
                color_array = []
                color_index = self.image_mode.index(char)
                side = "-" + char
                index = 0
                for x in self.image_array:
                    for y in x:
                        amplitude = self.get_amplitude(index)
                        color_array.append(
                            self.get_wave(
                                y[color_index], freq_range, amplitude, wave_type="sine"
                            )
                        )
                        index += 1
                self.save_wav(
                    self.path,
                    self.output,
                    side,
                    np.hstack((np.array(color_array).reshape(-1, 1),)),
                )

    def convert_to_stereo(self):
        if self.method2:
            left_freq_range = []
            right_freq_range = []
            for num in self.freq_dict:
                if num <= tone_array.FREQ_DICT["C5"]:
                    left_freq_range.append(num)
                elif tone_array.FREQ_DICT["C4"] <= num <= tone_array.FREQ_DICT["C7"]:
                    right_freq_range.append(num)
        else:
            left_freq_range = self.freq_dict
            right_freq_range = self.freq_dict
        with Halo(text="Converting data…", color="white"):
            left_data, right_data = [], []
            index = 0
            for x in self.image_array:
                for y in x:
                    amplitude = self.get_amplitude(index)
                    left_data.append(
                        self.get_wave(
                            (y[0] + y[1]) / 2,
                            left_freq_range,
                            amplitude,
                            wave_type="sine",
                        )
                    )
                    right_data.append(
                        self.get_wave(
                            (y[2] + y[1]) / 2,
                            right_freq_range,
                            amplitude,
                            wave_type="sine",
                        )
                    )
                    index += 1
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
        self.image_mode = img.mode
        if img.mode == "CMYK":
            print("CMYK format recognized - converting using 'quartet' mode")
            self.create_quartet()
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

    def create_quartet(self):
        cyan_freq_range = []
        magenta_freq_range = []
        yellow_freq_range = []
        black_freq_range = []
        for num in self.freq_dict:
            # These settings simulate the range of two violins, viola and cello
            if tone_array.FREQ_DICT["G3"] <= num <= tone_array.FREQ_DICT["A7"]:
                cyan_freq_range.append(num)
                magenta_freq_range.append(num)
            if tone_array.FREQ_DICT["C3"] <= num <= tone_array.FREQ_DICT["C7"]:
                yellow_freq_range.append(num)
            if tone_array.FREQ_DICT["C2"] <= num <= tone_array.FREQ_DICT["C6"]:
                black_freq_range.append(num)

        with Halo(text="Converting data…", color="white"):
            cyan_array, magenta_array, yellow_array, black_array = [], [], [], []
            index = 0
            for x in self.image_array:
                for y in x:
                    amplitude = self.get_amplitude(index)
                    cyan_array.append(
                        self.get_wave(
                            y[0], cyan_freq_range, amplitude, wave_type="sawtooth"
                        )
                    )
                    magenta_array.append(
                        self.get_wave(
                            y[1], magenta_freq_range, amplitude, wave_type="sawtooth"
                        )
                    )
                    yellow_array.append(
                        self.get_wave(
                            y[2], yellow_freq_range, amplitude, wave_type="sawtooth"
                        )
                    )
                    black_array.append(
                        self.get_wave(
                            y[3], black_freq_range, amplitude, wave_type="sawtooth"
                        )
                    )
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
