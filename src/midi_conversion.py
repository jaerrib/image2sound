# import math

from PIL import Image


# def frequency_to_midi(frequency: float) -> int:
#     midi_note = 69 + 12 * math.log2(frequency / 440.0)
#     return round(midi_note)


def create_array_from_image(img: Image.Image):
    pass


def midi_convert(sound_image) -> None:
    img: Image = sound_image.open_file()
    if img.mode not in ["RGB", "RGBA", "CMYK"]:
        print("Invalid image type. Please use an RGB, RGBA, or CMYK file.")
    else:
        if sound_image.reveal:
            sound_image.override(img)
        create_array_from_image(img)
        sound_image.image_mode = img.mode
        if img.mode == "CMYK":
            print("CMYK format recognized - converting using 'quartet' mode")
            pass
        elif sound_image.split:
            pass
        else:
            pass
    print("Midi function complete")
