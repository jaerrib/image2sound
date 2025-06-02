import math

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
from PIL import Image

import tone_array

TICKS_PER_BEAT = 480  # ticks per quarter note


def frequency_to_midi(frequency: float) -> int:
    midi_note = 69 + 12 * math.log2(frequency / 440.0)
    return round(midi_note)


def generate_note(sound_image, color_index, freq_range, track, y, note_length):
    freq = sound_image.get_freq(y[color_index], freq_range)
    note = frequency_to_midi(freq)
    on_time = 0
    off_time = note_length
    track.append(Message(type="note_on", note=note, velocity=64, time=on_time))
    track.append(
        Message(
            type="note_off",
            note=note,
            velocity=64,
            time=off_time,
        )
    )


def get_quartet_range(track_num, freq_dict):
    restricted_freq_dict = []
    for num in freq_dict:
        match track_num:
            case 0:
                if tone_array.FREQ_DICT["G3"] <= num <= tone_array.FREQ_DICT["A7"]:
                    restricted_freq_dict.append(num)
            case 1:
                if tone_array.FREQ_DICT["G3"] <= num <= tone_array.FREQ_DICT["A7"]:
                    restricted_freq_dict.append(num)
            case 2:
                if tone_array.FREQ_DICT["C3"] <= num <= tone_array.FREQ_DICT["C7"]:
                    restricted_freq_dict.append(num)
            case 3:
                if tone_array.FREQ_DICT["C2"] <= num <= tone_array.FREQ_DICT["C6"]:
                    restricted_freq_dict.append(num)
    return restricted_freq_dict


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
        note_length = round(TICKS_PER_BEAT / sound_image.time_signature[1])
        for track_num in range(num_tracks):
            freq_range = (
                get_quartet_range(track_num, sound_image.freq_dict)
                if img.mode == "CMYK"
                else sound_image.freq_dict
            )
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
            for x in sound_image.image_array:
                for y in x:
                    generate_note(
                        sound_image, track_num, freq_range, track, y, note_length
                    )

        midi_file.save("output.mid")

        print("Midi function complete")

        return
