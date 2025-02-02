import math
import os
from typing import Self

import numpy as np
import wavio
from PIL import Image
from halo import Halo
# noinspection PyProtectedMember
from mutagen.id3 import APIC
from mutagen.wave import WAVE

import dimension_calc
import tone_array
from envelope_settings import envelope_settings
from midi_conversion import midi_convert

RATE: int = 44100
DEFAULT_SETTINGS: dict = {
    "path": "test_image.png",
    "output": "",
    "key": "C-Major",
    "tempo": 60,
    "minutes": 1,
    "seconds": 0,
    "split": False,
    "reveal": False,
    "method2": False,
    "midi": False,
    "smooth": False,
    "time_signature": "4/4",
    "adsr": "piano",
    "waveform": "sine",
}


class SoundImage:
    def __init__(self, data) -> None:
        self.path: str = data["path"]
        self.output: str = data["output"]
        self.key: str = data["key"]
        self.freq_dict: list[float] = tone_array.get_tone_array(self.key)
        self.length: int = len(self.freq_dict)
        self.time_signature: list[int] = self.separate_time_signature(
            data["time_signature"]
        )
        self.tempo: int = data["tempo"]
        self.note_length: float = self.get_note_length()
        self.minutes: int = data["minutes"] + data["seconds"] / 60
        self.image_array: np.ndarray[float] | None = None
        self.split: bool = data["split"]
        self.reveal: bool = data["reveal"]
        self.overrides: list[str] = data["overrides"]
        self.method2: bool = data["method2"]
        self.midi: bool = data["midi"]
        self.smooth: bool = data["smooth"]
        self.image_mode: str | None = None
        self.adsr: str = data["adsr"]
        self.adsr_settings: dict = envelope_settings[self.adsr]
        self.waveform: str = data["waveform"]

    def open_file(self) -> Image:
        return Image.open(self.path)

    def image_to_array(self, img: Image.Image) -> Self:
        self.image_array = np.asarray(
            img.resize(
                dimension_calc.get_new_dim(
                    img.size, self.minutes, self.tempo, self.time_signature
                )
            ),
            dtype="int64",
        )
        return self

    def get_note_length(self) -> float:
        duration = 60 / self.tempo
        note_length = duration / self.time_signature[1]
        return note_length

    @staticmethod
    def separate_time_signature(time_signature: str) -> list[int]:
        top, bottom = time_signature.split("/")
        top, bottom = int(top), int(bottom)
        if top == 0:
            top = 1
        if bottom == 0:
            bottom = 1
        split_time_signature = [top, bottom]
        return split_time_signature

    @staticmethod
    def get_freq(color: int, freq_range) -> float:
        return freq_range[math.trunc(color / (256 / len(freq_range))) - 1]

    @staticmethod
    def apply_blackman(wave: np.ndarray) -> np.ndarray:
        # Optionally apply the Blackman smoothing window
        blackman_window = np.blackman(len(wave))
        wave *= blackman_window
        return wave

    def get_envelope(self, amplitude: float) -> np.ndarray:
        attack: float = self.adsr_settings["a"] * self.note_length
        decay: float = self.adsr_settings["d"] * self.note_length
        sustain: float = self.adsr_settings["s"] * amplitude
        sustain_level: float = sustain
        release: float = self.adsr_settings["r"] * self.note_length
        sample_rate: int = RATE

        total_samples = int(RATE * self.note_length)
        attack_samples = int(attack * sample_rate)
        decay_samples = int(decay * sample_rate)
        release_samples = int(release * sample_rate)
        sustain_samples: int = total_samples - (
            attack_samples + decay_samples + release_samples
        )

        envelope = np.zeros(total_samples)
        envelope[:attack_samples] = np.linspace(0, amplitude, attack_samples)
        envelope[attack_samples : attack_samples + decay_samples] = np.linspace(
            amplitude, sustain_level, decay_samples
        )
        envelope[
            attack_samples
            + decay_samples : attack_samples
            + decay_samples
            + sustain_samples
        ] = sustain
        envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)

        return envelope

    def get_wave(
        self, color: int, freq_range: list[float], amplitude: float, wave_type: str
    ) -> np.ndarray:
        freq = self.get_freq(color, freq_range)
        t = np.linspace(
            0, self.note_length, int(RATE * self.note_length), endpoint=False
        )
        envelope = self.get_envelope(amplitude)

        match wave_type:
            case "sine":
                wave = amplitude * (np.sin(2 * np.pi * t * freq))
                for k in range(1, 6):
                    wave += amplitude * (1 / k) * np.sin(2 * np.pi * k * freq * t)
            case "square":
                wave = amplitude * 0.5 * (1 + np.sign(np.sin(2 * np.pi * freq * t)))
                for k in range(1, 10, 2):
                    wave += amplitude * (1 / k) * np.sin(2 * np.pi * k * freq * t)
            case "triangle":
                wave = amplitude * (
                    2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
                )
                for k in range(1, 10, 2):
                    harmonic = amplitude * (
                        (8 / (np.pi**2))
                        * ((-1) ** ((k - 1) // 2) / k**2)
                        * np.sin(2 * np.pi * k * freq * t)
                    )
                    wave += harmonic
            case "sawtooth":
                wave = amplitude * 2 * (t * freq - np.floor(0.5 + t * freq))
                for k in range(2, 20):
                    wave += (
                        (amplitude / k)
                        * 2
                        * (t * k * freq - np.floor(0.5 + t * k * freq))
                    )
                wave = wave / np.max(np.abs(wave))
            case "piano":
                wave = np.sin(2 * np.pi * freq * t)
                wave += amplitude * 0.5 * np.sin(2 * np.pi * 2 * freq * t)
                wave += amplitude * 0.25 * np.sin(2 * np.pi * 3 * freq * t)
                wave += amplitude * 0.125 * np.sin(2 * np.pi * 4 * freq * t)
            case _:
                wave = amplitude * (np.sin(2 * np.pi * t * freq))
        wave = wave * envelope
        if self.smooth:
            wave = self.apply_blackman(wave)
        return wave

    @staticmethod
    def save_wav(input_path: str, output_path: str, side: str, array) -> None:
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

    def get_amplitude(self, index: int) -> float:
        # Accents the first beat of each measure by applying a higher amplitude
        if index % self.time_signature[0] == 0:
            return 0.7
        return 0.5

    def convert_to_multiple(self) -> None:
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
                                y[color_index],
                                freq_range,
                                amplitude,
                                wave_type=self.waveform,
                            )
                        )
                        index += 1
                self.save_wav(
                    self.path,
                    self.output,
                    side,
                    np.hstack((np.array(color_array).reshape(-1, 1),)),
                )

    def convert_to_stereo(self) -> None:
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
                            wave_type=self.waveform,
                        )
                    )
                    right_data.append(
                        self.get_wave(
                            (y[2] + y[1]) / 2,
                            right_freq_range,
                            amplitude,
                            wave_type=self.waveform,
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

    def convert(self) -> None:
        if self.midi:
            midi_convert(self)
        else:
            img: Image = self.open_file()
            if img.mode not in ["RGB", "RGBA", "CMYK"]:
                print("Invalid image type. Please use an RGB, RGBA, or CMYK file.")
            else:
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

    def determine_key(self, red: int, green: int, blue: int) -> Self:
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

    def override(self, img: Image.Image) -> Self:
        tiny_img_arr = np.asarray(img.resize((1, 1)), dtype="int64")
        red = int(tiny_img_arr[0][0][0])
        green = int(tiny_img_arr[0][0][1])
        blue = int(tiny_img_arr[0][0][2])
        if "tempo" in self.overrides:
            self.tempo = (red + green + blue) / 3
        if "key" in self.overrides:
            self.determine_key(red=red, green=green, blue=blue)
        if "minutes" in self.overrides and "seconds" in self.overrides:
            self.minutes = math.sqrt((img.size[0] + img.size[1]) / 2) / 2
        return self

    def create_quartet(self) -> None:
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
                    self.adsr_settings = envelope_settings["violin"]
                    cyan_array.append(
                        self.get_wave(
                            y[0], cyan_freq_range, amplitude, wave_type=self.waveform
                        )
                    )
                    magenta_array.append(
                        self.get_wave(
                            y[1], magenta_freq_range, amplitude, wave_type=self.waveform
                        )
                    )
                    self.adsr_settings = envelope_settings["viola"]
                    yellow_array.append(
                        self.get_wave(
                            y[2], yellow_freq_range, amplitude, wave_type=self.waveform
                        )
                    )
                    self.adsr_settings = envelope_settings["cello"]
                    black_array.append(
                        self.get_wave(
                            y[3], black_freq_range, amplitude, wave_type=self.waveform
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
