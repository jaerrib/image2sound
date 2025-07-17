import math

import numpy as np
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
from PIL import Image

import comp_engine

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


def midi_convert(sound_image) -> None:
    movement_style: str = (
        "sonata"  # placeholder until parameter settings is implemented
    )
    img: Image = sound_image.open_file()
    if img.mode not in ["RGB", "RGBA", "CMYK"]:
        print("Invalid image type. Please use an RGB, RGBA, or CMYK file.")
    else:
        if sound_image.reveal:
            sound_image.override(img)
        sound_image.image_to_array(img)
        sound_image.image_mode = img.mode
        midi_file = MidiFile(ticks_per_beat=TICKS_PER_BEAT, type=1)

        num_tracks: int = 4 if img.mode == "CMYK" else 3

        midi_tempo: int = bpm2tempo(sound_image.tempo)
        for track_num in range(num_tracks):
            freq_range: list[float] = sound_image.get_freq_range(img.mode[track_num])
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
            flat_array: list = flatten_image_array(sound_image.image_array, track_num)
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


def get_note_length(track_num: int, index: int, note_length: float) -> float:
    match track_num:
        case 1:
            if index % 2 == 0:
                return note_length * 2
            else:
                return 0
        case 2:
            if index % 4 == 0:
                return note_length * 4
            else:
                return 0
        case 3:
            if index % 8 == 0:
                return note_length * 8
            else:
                return 0
        case _:
            return note_length


def flatten_image_array(image_array, track_num: int) -> list:
    if image_array is None:
        raise ValueError(
            "image_array is None. Check if sound_image.image_to_array() is working correctly."
        )
    image_array = np.array(image_array)
    flattened_array = image_array.reshape(-1, image_array.shape[-1])
    color_array: list = [pixel[track_num] for pixel in flattened_array]
    return color_array
