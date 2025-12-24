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
    flatten_image_array,
    get_avg_color_dif,
    midi_convert,
    tempo_marking,
    total_measures_from_movement,
)
from movement_definitions import movement_type

RATE: int = 44100
DEFAULT_SETTINGS: dict = {
    "path": "test_image.png",
    "output": "",
    "key": "C-Major",
    "tempo": 60,
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
        self.image_array: list | None = None
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

    def open_file(self) -> Image.Image:
        return Image.open(self.path)

    def image_to_array(self, img: Image.Image) -> Self:
        total_measures: int = total_measures_from_movement(self.movement_type)
        max_notes: int = total_measures * comp_engine.NOTES_PER_MEASURE
        optimal_dim: int = math.floor(math.sqrt(max_notes))
        self.image_array: np.ndarray = np.asarray(
            img.resize((optimal_dim, optimal_dim)), dtype="int64"
        )
        return self

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
        # Convert color (0-255) to an index in the freq_range
        index = min(math.trunc(color / (256 / len(freq_range))), len(freq_range) - 1)
        return freq_range[index]

    @staticmethod
    def apply_blackman(wave: np.ndarray) -> np.ndarray:
        # Optionally apply the Blackman smoothing window
        blackman_window: np.ndarray = np.blackman(len(wave))
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
        wave: np.ndarray = amplitude * np.sin(2 * np.pi * freq * t)
        for k in range(1, 6):
            wave += amplitude * (1 / k) * np.sin(2 * np.pi * k * freq * t)
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val
        return wave

    @staticmethod
    def create_square_wave(amplitude: float, freq: float, t: np.ndarray) -> np.ndarray:
        wave: np.ndarray = amplitude * 0.5 * (1 + np.sign(np.sin(2 * np.pi * freq * t)))
        for k in range(1, 10, 2):
            wave += amplitude * (1 / k) * np.sin(2 * np.pi * k * freq * t)
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val
        return wave

    @staticmethod
    def create_sawtooth_wave(
        amplitude: float, freq: float, t: np.ndarray
    ) -> np.ndarray:
        wave: np.ndarray = amplitude * 2 * (t * freq - np.floor(0.5 + t * freq))
        for k in range(2, 20):
            wave += (amplitude / k) * 2 * (t * k * freq - np.floor(0.5 + t * k * freq))
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val
        return wave

    @staticmethod
    def create_triangle_wave(
        amplitude: float, freq: float, t: np.ndarray
    ) -> np.ndarray:
        wave: np.ndarray = amplitude * (
            2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
        )
        for k in range(1, 10, 2):
            harmonic = amplitude * (
                (8 / (np.pi**2))
                * ((-1) ** ((k - 1) // 2) / k**2)
                * np.sin(2 * np.pi * k * freq * t)
            )
            wave += harmonic
        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val
        return wave

    @staticmethod
    def create_piano_wave(amplitude: float, freq: float, t: np.ndarray) -> np.ndarray:
        wave: np.ndarray = np.sin(2 * np.pi * freq * t)
        wave += amplitude * 0.5 * np.sin(2 * np.pi * 2 * freq * t)
        wave += amplitude * 0.25 * np.sin(2 * np.pi * 3 * freq * t)
        wave += amplitude * 0.125 * np.sin(2 * np.pi * 4 * freq * t)
        return wave

    def save_wav(self, side: str, array) -> None:
        tempo: str = tempo_marking(self.tempo)
        file_name: str = (
            ".".join(self.path.split(".")[:-1]).split("/")[-1]
            + f", {self.movement_type.capitalize()} in {self.key} ({tempo}){side}.wav"
        )
        if self.output == "":
            pass
        elif os.path.isdir(self.output):
            file_name = self.output + file_name
        else:
            file_name = file_name
        with Halo(text="Saving file…", color="white"):
            wavio.write(file_name, array, RATE, scale=2, sampwidth=3, clip="ignore")
            audio_file = WAVE(file_name)
            audio_file.add_tags()
            audio_file.tags.add(
                APIC(
                    encoding=3,  # 3 is for utf-8
                    mime=f"image/{Image.open(self.path).format.lower()}",  # can be image/jpeg or image/png
                    type=3,  # 3 is for the cover image
                    desc="Cover",
                    data=open(self.path, mode="rb").read(),
                )
            )
            audio_file.save()
        print("Saved file as " + file_name)

    def get_amplitude(self, index: int) -> float:
        # Accents the first beat of each measure by applying higher amplitude
        if index % self.time_signature[0] == 0:
            return 0.7
        return 0.5

    def convert(self) -> None:
        if self.midi:
            midi_convert(self)
        else:
            img: Image.Image = self.open_file()
            if img.mode not in ["RGB", "RGBA", "CMYK"]:
                print("Invalid image type. Please use an RGB, RGBA, or CMYK file.")
            else:
                if self.reveal:
                    self.override(img)
                self.image_to_array(img)
                self.image_mode = img.mode
                self.convert_with_comp_engine()

    def determine_key(self, red: int, green: int, blue: int) -> Self:
        notes: list[str] = tone_array.get_chromatic_notes()
        key: str = notes[math.trunc(red / (255 / len(notes)))] + (
            "Major" if blue % 2 == 0 else "Minor"
        )
        if not math.isclose(math.sqrt(red * green * blue) % 1, 0):
            key = notes[math.trunc(red / (255 / len(notes)))] + "8Tone"
        elif green % 16 == 0:
            key += "Pentatonic"
        self.key = key
        return self

    def override(self, img: Image.Image) -> Self:
        tiny_img_arr: np.ndarray = np.asarray(img.resize((1, 1)), dtype="int64")
        red = int(tiny_img_arr[0][0][0])
        green = int(tiny_img_arr[0][0][1])
        blue = int(tiny_img_arr[0][0][2])
        if "tempo" in self.overrides:
            self.tempo = (red + green + blue) // 3
        if "key" in self.overrides:
            self.determine_key(red=red, green=green, blue=blue)
        if "movement_type" in self.overrides:
            movements = list(movement_type.keys())
            avg_color: float = (red + green + blue) / 3
            self.movement_type = movements[
                math.trunc(avg_color / (255 / len(movements)))
            ]
        return self

    def get_freq_range(self, char: str) -> list[float]:
        freq_range: list[float] = []
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
                case "G" | "B" if (
                    tone_array.FREQ_DICT["C4"] <= num <= tone_array.FREQ_DICT["C7"]
                ):
                    freq_range.append(num)
                case _:
                    freq_range.append(num)
        return freq_range

    def convert_with_comp_engine(self) -> None:
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
                                self.generate_wave(track_num, value, length)
                            )
                color = "-" + char
                self.save_wav(
                    color,
                    array=np.concatenate(color_array).reshape(-1, 1),
                )

    def generate_wave(self, track_num, freq, length) -> np.ndarray:
        amplitude: float = self.get_amplitude(track_num)
        # Calculate the duration in seconds for a sixteenth note at the current tempo
        sixteenth_duration: float = 60.0 / (
            self.tempo * 4
        )  # quarter note duration divided by 4
        # Total duration for this note based on its length in sixteenth notes
        note_duration: float = sixteenth_duration * length
        num_samples = int(RATE * note_duration)
        if num_samples <= 0:
            num_samples = 1

        t = np.linspace(0, note_duration, num_samples, endpoint=False)
        envelope: np.ndarray = self.get_envelope(amplitude, note_duration)
        wave: np.ndarray = np.zeros(1)
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
        wave *= envelope
        if self.smooth:
            wave = self.apply_blackman(wave)
        return wave
