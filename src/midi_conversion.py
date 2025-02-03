import math

from PIL import Image

TICKS_PER_BEAT = 480  # ticks per quarter note


def frequency_to_midi(frequency: float) -> int:
    midi_note = 69 + 12 * math.log2(frequency / 440.0)
    return round(midi_note)


def generate_json_from_image_data(sound_image):
    # microseconds_per_beat = 60000000 // sound_image.tempo
    freq_range = sound_image.freq_dict
    midi_data = {"ticks_per_beat": 480, "tracks": []}
    for color in sound_image.image_mode:
        track = {"messages": []}
        color_index = sound_image.image_mode.index(color)
        index = 0
        for x in sound_image.image_array:
            for y in x:
                freq = sound_image.get_freq(y[color_index], freq_range)
                note = frequency_to_midi(freq)
                on_msg = {"type": "note_on", "note": note, "velocity": 64, "time": 0}
                off_msg = {
                    "type": "note_off",
                    "note": note,
                    "velocity": 64,
                    "time": 480,
                }
                track["messages"].append(on_msg)
                track["messages"].append(off_msg)
                index += 1
        midi_data["tracks"].append(track)
    print(midi_data)


def midi_convert(sound_image) -> None:
    img: Image = sound_image.open_file()
    if img.mode not in ["RGB", "RGBA", "CMYK"]:
        print("Invalid image type. Please use an RGB, RGBA, or CMYK file.")
    else:
        if sound_image.reveal:
            sound_image.override(img)
        sound_image.image_to_array(img)
        sound_image.image_mode = img.mode
        generate_json_from_image_data(sound_image)
        # if img.mode == "CMYK":
        #     print("CMYK format recognized - converting using 'quartet' mode")
        #     pass
        # elif sound_image.split:
        #     pass
        # else:
        #     pass
    print("Midi function complete")
