import math
import os
import sys
from typing import Self

import numpy as np
import wavio
from halo import Halo

# noinspection PyProtectedMember
from mutagen.id3 import APIC
from mutagen.wave import WAVE
from PIL import Image

import comp_engine
import tone_array
from envelope_settings import envelope_settings
from midi_conversion import (
    midi_convert,
    flatten_image_array,
    get_avg_color_dif,
    total_measures_from_movement,
)
from movement_definitions import movement_type

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
    "movement_type": "sonata",
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
        self.image_array: list | None = None
        self.split: bool = data["split"]
        self.reveal: bool = data["reveal"]
        self.overrides: list[str] = data["overrides"]
        self.method2: bool = data["method2"]
        self.midi: bool = data["midi"]
        self.movement_type: str = data["movement_type"]
        self.smooth: bool = data["smooth"]
        self.image_mode: str | None = None
        self.adsr: str = data["adsr"]
        self.adsr_settings: dict = envelope_settings[self.adsr]
        self.waveform: str = data["waveform"]

    def open_file(self) -> Image:
        return Image.open(self.path)

    def image_to_array(self, img: Image.Image) -> Self:
        total_measures: int = total_measures_from_movement(self.movement_type)
        max_notes: int = total_measures * comp_engine.NOTES_PER_MEASURE
        optimal_dim: int = math.floor(math.sqrt(max_notes))
        self.image_array = np.asarray(
            img.resize((optimal_dim, optimal_dim)), dtype="int64"
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
    def get_freq(color: int, freq_range: list[float]) -> float:
        # Convert color (0-255) to MIDI note first
        midi_note = (
            math.trunc(color / (256 / len(freq_range))) + 60
        )  # Start from middle-C (60)
        # Convert MIDI note to frequency
        return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

    @staticmethod
    def apply_blackman(wave: np.ndarray) -> np.ndarray:
        # Optionally apply the Blackman smoothing window
        blackman_window = np.blackman(len(wave))
        wave *= blackman_window
        return wave

    def get_envelope(self, amplitude: float, length: float) -> np.ndarray:
        attack: float = self.adsr_settings["a"] * length
        decay: float = self.adsr_settings["d"] * length
        sustain: float = self.adsr_settings["s"] * amplitude
        sustain_level: float = sustain
        release: float = self.adsr_settings["r"] * length
        sample_rate: int = RATE

        total_samples = int(RATE * length)
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

    @staticmethod
    def create_sine_wave(amplitude: float, freq: float, t: np.ndarray) -> np.ndarray:
        wave = amplitude * (np.sin(2 * np.pi * t * freq))
        for k in range(1, 6):
            wave += amplitude * (1 / k) * np.sin(2 * np.pi * k * freq * t)
        return wave

    @staticmethod
    def create_square_wave(amplitude: float, freq: float, t: np.ndarray) -> np.ndarray:
        wave = amplitude * 0.5 * (1 + np.sign(np.sin(2 * np.pi * freq * t)))
        for k in range(1, 10, 2):
            wave += amplitude * (1 / k) * np.sin(2 * np.pi * k * freq * t)
        return wave

    @staticmethod
    def create_sawtooth_wave(
        amplitude: float, freq: float, t: np.ndarray
    ) -> np.ndarray:
        wave = amplitude * 2 * (t * freq - np.floor(0.5 + t * freq))
        for k in range(2, 20):
            wave += (amplitude / k) * 2 * (t * k * freq - np.floor(0.5 + t * k * freq))
        wave = wave / np.max(np.abs(wave))
        return wave

    @staticmethod
    def create_triangle_wave(
        amplitude: float, freq: float, t: np.ndarray
    ) -> np.ndarray:
        wave = amplitude * (2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1)
        for k in range(1, 10, 2):
            harmonic = amplitude * (
                (8 / (np.pi**2))
                * ((-1) ** ((k - 1) // 2) / k**2)
                * np.sin(2 * np.pi * k * freq * t)
            )
            wave += harmonic
        return wave

    @staticmethod
    def create_piano_wave(amplitude: float, freq: float, t: np.ndarray) -> np.ndarray:
        wave = np.sin(2 * np.pi * freq * t)
        wave += amplitude * 0.5 * np.sin(2 * np.pi * 2 * freq * t)
        wave += amplitude * 0.25 * np.sin(2 * np.pi * 3 * freq * t)
        wave += amplitude * 0.125 * np.sin(2 * np.pi * 4 * freq * t)
        return wave

    def get_wave(
        self, color: int, freq_range: list[float], amplitude: float, wave_type: str
    ) -> np.ndarray:
        freq = self.get_freq(color, freq_range)
        t = np.linspace(
            0, self.note_length, int(RATE * self.note_length), endpoint=False
        )
        envelope = self.get_envelope(amplitude, self.note_length)

        match wave_type:
            case "sine":
                wave = self.create_sine_wave(amplitude, freq, t)
            case "square":
                wave = self.create_square_wave(amplitude, freq, t)
            case "triangle":
                wave = self.create_triangle_wave(amplitude, freq, t)
            case "sawtooth":
                wave = self.create_sawtooth_wave(amplitude, freq, t)
            case "piano":
                wave = self.create_piano_wave(amplitude, freq, t)
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
        # Accents the first beat of each measure by applying higher amplitude
        if index % self.time_signature[0] == 0:
            return 0.7
        return 0.5

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
                if img.mode == "CMYK" or self.split:
                    self.convert_with_comp_engine()
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

    def generate_color_array(self, char: str, freq_range: list) -> list:
        color_array = []
        color_index = self.image_mode.index(char)
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
        return color_array

    def get_freq_range(self, char: str) -> list:
        freq_range = []
        for num in self.freq_dict:
            match char:
                case "C" | "R" if not self.method2:
                    # Limits range to the 3rd position of violin
                    if tone_array.FREQ_DICT["C4"] <= num <= tone_array.FREQ_DICT["D#6"]:
                        freq_range.append(num)
                case "M" | "A":
                    # Limits range to 1st position of violin
                    if tone_array.FREQ_DICT["G3"] <= num <= tone_array.FREQ_DICT["B5"]:
                        freq_range.append(num)
                case "Y" | "G" if not self.method2:
                    # Limits range to 1st position of viola
                    if tone_array.FREQ_DICT["C3"] <= num <= tone_array.FREQ_DICT["E5"]:
                        freq_range.append(num)
                case "K" | "B" if not self.method2:
                    # Limits range to 1st position of cello
                    if tone_array.FREQ_DICT["C2"] <= num <= tone_array.FREQ_DICT["D#4"]:
                        freq_range.append(num)
                case "R" if num <= tone_array.FREQ_DICT["C5"]:
                    freq_range.append(num)
                case "G" if (
                    tone_array.FREQ_DICT["C4"] <= num <= tone_array.FREQ_DICT["C7"]
                ):
                    freq_range.append(num)
                case "B" if (
                    tone_array.FREQ_DICT["C4"] <= num <= tone_array.FREQ_DICT["C7"]
                ):
                    freq_range.append(num)
                case _:
                    freq_range.append(num)
        return freq_range

    def convert_with_comp_engine(self):
        movement_style: str = self.movement_type
        if movement_style not in movement_type:
            print(
                f"Unsupported movement type: '{movement_style}'. Available types are: {list(movement_type.keys())}"
            )
            sys.exit(1)
        with Halo(text="Converting data…", color="white"):
            num_tracks: int = 4 if self.image_mode == "CMYK" else 3
            for track_num in range(num_tracks):
                char: str = self.image_mode[track_num]
                flat_array: list = flatten_image_array(self.image_array, track_num)
                avg_color_dif = get_avg_color_dif(flat_array)
                new_movement: dict = comp_engine.generate_movement(
                    movement_style, flat_array, avg_color_dif
                )
                color_array = []
                for section_label, phrases in new_movement.items():
                    for phrase in phrases:
                        for value, length in phrase:
                            color_array.append(
                                self.generate_note(track_num, value, length)
                            )
                color = "-" + char
                self.save_wav(
                    self.path,
                    self.output,
                    color,
                    array=np.concatenate(color_array).reshape(-1, 1),
                )

    def generate_note(self, track_num, freq, length):
        amplitude = self.get_amplitude(track_num)
        # Calculate the duration in seconds for a sixteenth note at the current tempo
        sixteenth_duration = 60.0 / (
            self.tempo * 4
        )  # quarter note duration divided by 4
        # Total duration for this note based on its length in sixteenth notes
        note_duration = sixteenth_duration * length
        num_samples = int(RATE * note_duration)
        if num_samples <= 0:
            num_samples = 1

        t = np.linspace(0, note_duration, num_samples, endpoint=False)
        envelope = self.get_envelope(amplitude, note_duration)

        match self.waveform:
            case "sine":
                wave = self.create_sine_wave(amplitude, freq, t)
            case "square":
                wave = self.create_square_wave(amplitude, freq, t)
            case "triangle":
                wave = self.create_triangle_wave(amplitude, freq, t)
            case "sawtooth":
                wave = self.create_sawtooth_wave(amplitude, freq, t)
            case "piano":
                wave = self.create_piano_wave(amplitude, freq, t)
            case _:
                wave = amplitude * (np.sin(2 * np.pi * t * freq))
        wave = wave * envelope
        if self.smooth:
            wave = self.apply_blackman(wave)
        # Ensure the wave array is not empty
        if len(wave) == 0:
            wave = np.zeros(1)
        return wave
