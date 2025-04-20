import math

from PIL import Image
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo

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


def midi_convert(sound_image) -> None:
    img: Image = sound_image.open_file()
    if img.mode not in ["RGB", "RGBA", "CMYK"]:
        print("Invalid image type. Please use an RGB, RGBA, or CMYK file.")
    else:
        if sound_image.reveal:
            sound_image.override(img)
        sound_image.image_to_array(img)
        sound_image.image_mode = img.mode
        freq_range = sound_image.freq_dict
        midi_file = MidiFile(ticks_per_beat=TICKS_PER_BEAT, type=1)

        track1 = MidiTrack()
        track2 = MidiTrack()
        track3 = MidiTrack()
        midi_file.tracks.append(track1)
        midi_file.tracks.append(track2)
        midi_file.tracks.append(track3)

        track1.append(
            MetaMessage(
                "time_signature",
                numerator=sound_image.time_signature[0],
                denominator=sound_image.time_signature[1],
            )
        )
        track2.append(
            MetaMessage(
                "time_signature",
                numerator=sound_image.time_signature[0],
                denominator=sound_image.time_signature[1],
            )
        )
        track3.append(
            MetaMessage(
                "time_signature",
                numerator=sound_image.time_signature[0],
                denominator=sound_image.time_signature[1],
            )
        )

        midi_tempo = bpm2tempo(sound_image.tempo)
        track1.append(
            MetaMessage(
                "set_tempo",
                tempo=midi_tempo,
            )
        )
        track2.append(
            MetaMessage(
                "set_tempo",
                tempo=midi_tempo,
            )
        )
        track3.append(
            MetaMessage(
                "set_tempo",
                tempo=midi_tempo,
            )
        )

        track1.append(Message("control_change", control=10, value=0))
        track2.append(Message("control_change", control=10, value=64))
        track3.append(Message("control_change", control=10, value=127))

        note_length = round(TICKS_PER_BEAT / sound_image.time_signature[1])

        for x in sound_image.image_array:
            for y in x:
                generate_note(sound_image, 0, freq_range, track1, y, note_length)
                generate_note(sound_image, 1, freq_range, track2, y, note_length)
                generate_note(sound_image, 2, freq_range, track3, y, note_length)

        midi_file.save("output.mid")

        print("Midi function complete")

        return
