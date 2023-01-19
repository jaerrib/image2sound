from PIL import Image
import numpy as np
import wavio
import argparse
from math import trunc


def image_to_array(save_path):
    img = Image.open(save_path).convert(mode="RGB")
    img_arr = np.asarray(img, dtype='int64')
    return img_arr


def rgb_to_frequency(r, g, b):
    red_dict = {
        "0": 130.8128,
        "1": 146.8324,
        "2": 164.8138,
        "3": 174.6141,
        "4": 195.9977,
        "5": 220.0000,
        "6": 246.9417,
    }

    green_dict = {
        "0": 261.6256,
        "1": 293.6646,
        "2": 329.6276,
        "3": 349.2282,
        "4": 391.9954,
        "5": 440.0000,
        "6": 493.8833,
    }

    blue_dict = {
        "0": 523.2511,
        "1": 587.3295,
        "2": 659.4565,
        "3": 698.4565,
        "4": 783.9909,
        "5": 880.0000,
        "6": 987.7666,
    }

    main_color = max(r, g, b)
    key_item = str(trunc(main_color / 37))
    if main_color == r:
        return red_dict[key_item]
    elif main_color == g:
        return green_dict[key_item]
    elif main_color == b:
        return blue_dict[key_item]


def array_to_sound(array):
    temp_array = []
    for x in array:
        for y in x:
            red = y[0]
            green = y[1]
            blue = y[2]
            freq = rgb_to_frequency(red, green, blue)
            tone = np.sin(2 * np.pi * freq)
            temp_array.append(tone)
    return temp_array


def save_wav(save_path, array):
    rate = 22050
    split_test = save_path.split(".")
    file_name = split_test[0]+".wav"
    wavio.write(file_name, array, rate, sampwidth=4, scale=2, clip="ignore")
    print("Saved file as ", file_name)


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str)
args = parser.parse_args()
path = args.path
image_array = image_to_array(path)
sound_array = array_to_sound(image_array)
save_wav(path, sound_array)
