import math
import sys

import numpy as np
from halo import Halo
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
from PIL import Image

import comp_engine
from movement_definitions import movement_type

TICKS_PER_BEAT: int = 480  # ticks per quarter note


def frequency_to_midi(frequency: float) -> int:
    midi_note: float = 69 + 12 * math.log2(frequency / 440.0)
    return round(midi_note)


def generate_note(
    sound_image,
    channel: int,
    freq_range: list[float],
    track: MidiTrack,
    y: int,
    note_length: int,
) -> None:
    freq: float = sound_image.get_freq(y, freq_range)
    note: int = frequency_to_midi(freq)
    on_time: int = 0
    off_time: int = note_length * int(TICKS_PER_BEAT / 4)
    track.append(
        Message(type="note_on", note=note, velocity=64, time=on_time, channel=channel)
    )
    track.append(
        Message(type="note_off", note=note, velocity=64, time=off_time, channel=channel)
    )


def total_measures_from_movement(movement_name: str) -> int:
    movement: dict = movement_type[movement_name]
    phrase_lengths = {
        phrase["label"]: phrase["length"] for phrase in movement["phrases"]
    }
    total_measures: int = 0
    for section in movement["sections"]:
        for phrase_label in section["sequence"]:
            length = phrase_lengths.get(phrase_label)
            if length is None:
                raise ValueError(f"Phrase '{phrase_label}' not found in phrases")
            total_measures += length
    return total_measures


def determine_optimum_size(movement_data) -> int:
    total_measures: int = total_measures_from_movement(movement_data)
    max_notes: int = total_measures * comp_engine.NOTES_PER_MEASURE
    dimension: int = math.floor(math.sqrt(max_notes))
    return dimension


def image_to_midi_array(img: Image.Image, movement_data: str) -> np.ndarray:
    optimal_dim = determine_optimum_size(movement_data)
    resized_img = img.resize((optimal_dim, optimal_dim))
    return np.asarray(resized_img, dtype="int64")


def midi_convert(sound_image) -> None:
    movement_style: str = sound_image.movement_type
    if movement_style not in movement_type:
        print(
            f"Unsupported movement type: '{movement_style}'. Available types are: {list(movement_type.keys())}"
        )
        sys.exit(1)
    with Halo(text="Converting data…", color="white"):
        img: Image = sound_image.open_file()
        if img.mode not in ["RGB", "RGBA", "CMYK"]:
            print("Invalid image type. Please use an RGB, RGBA, or CMYK file.")
        else:
            if sound_image.reveal:
                sound_image.override(img)
            sound_image.image_array = image_to_midi_array(img, movement_style)
            sound_image.image_mode = img.mode
            midi_file = MidiFile(ticks_per_beat=TICKS_PER_BEAT, type=1)

            num_tracks: int = 4 if img.mode == "CMYK" else 3

            midi_tempo: int = bpm2tempo(sound_image.tempo)
            for track_num in range(num_tracks):
                freq_range: list[float] = sound_image.get_freq_range(
                    img.mode[track_num]
                )
                track: MidiTrack = MidiTrack()
                midi_file.tracks.append(track)
                track.append(
                    MetaMessage(
                        "time_signature",
                        numerator=sound_image.time_signature[0],
                        denominator=sound_image.time_signature[1],
                    )
                )
                track.append(
                    MetaMessage(
                        "set_tempo",
                        tempo=midi_tempo,
                    )
                )
                pan_value: int = round((127 / num_tracks) * track_num)
                track.append(
                    Message(
                        "control_change", control=10, value=pan_value, channel=track_num
                    )
                )
                program_value: int = get_program_instrument(img.mode, track_num)
                track.append(
                    Message("program_change", program=program_value, channel=track_num)
                )
                flat_array: list = flatten_image_array(
                    sound_image.image_array, track_num
                )
                new_movement: dict = comp_engine.generate_movement(
                    movement_style, flat_array
                )

                for section_label, phrases in new_movement.items():
                    for phrase in phrases:
                        for value, length in phrase:
                            generate_note(
                                sound_image, track_num, freq_range, track, value, length
                            )
            midi_file.save("output.mid")
            print("Midi function complete")


def get_program_instrument(image_mode, track_num: int) -> int:
    channel_value: str = image_mode[track_num]
    match channel_value:
        case "C" | "M" | "R":
            return 40
        case "Y" | "G":
            return 41
        case "K" | "B" | "A":
            return 42
        case _:
            return 0


def flatten_image_array(image_array, track_num: int) -> list:
    if image_array is None:
        raise ValueError(
            "image_array is None. Check if sound_image.image_to_array() is working correctly."
        )
    image_array = np.array(image_array)
    flattened_array = image_array.reshape(-1, image_array.shape[-1])
    color_array: list = [pixel[track_num] for pixel in flattened_array]
    return color_array
