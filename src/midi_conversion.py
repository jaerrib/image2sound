import math

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
from PIL import Image

import comp_engine
import movement_definitions

TICKS_PER_BEAT = 480  # ticks per quarter note


def frequency_to_midi(frequency: float) -> int:
    midi_note = 69 + 12 * math.log2(frequency / 440.0)
    return round(midi_note)


def generate_note(sound_image, _color_index, freq_range, track, y, note_length):
    freq = sound_image.get_freq(y, freq_range)
    note = frequency_to_midi(freq)
    on_time = 0
    off_time = note_length * int(TICKS_PER_BEAT / 4)
    track.append(Message(type="note_on", note=note, velocity=64, time=on_time))
    track.append(
        Message(
            type="note_off",
            note=note,
            velocity=64,
            time=off_time,
        )
    )


def midi_convert(sound_image) -> None:
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

        midi_tempo = bpm2tempo(sound_image.tempo)
        for track_num in range(num_tracks):
            freq_range = sound_image.get_freq_range(img.mode[track_num])
            track = MidiTrack()
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
            track.append(Message("control_change", control=10, value=pan_value))
            flat_array = flatten_image_array(sound_image.image_array, track_num)
            new_movement = comp_engine.generate_movement(
                movement_definitions.movement_type["minuet"], flat_array
            )
            for section_label, phrases in new_movement.items():
                for phrase_label, notes in phrases.items():
                    for value, length in notes:
                        generate_note(
                            sound_image, track_num, freq_range, track, value, length
                        )
        midi_file.save("output.mid")
        print("Midi function complete")
        return


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


def flatten_image_array(image_array, track_num):
    flattened_array = image_array.reshape(-1, image_array.shape[-1])
    color_array = []
    for pixel in flattened_array:
        color_array.append(pixel[track_num])
    return color_array
