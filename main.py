from PIL import Image
import numpy as np
import wavio
import argparse


def image_to_array(save_path):
    img = Image.open(save_path).convert(mode="RGB")
    img_arr = np.asarray(img, dtype='int64')
    return img_arr


def rgb_to_frequency(r, g, b):
    freq = (r * g * b) / 829.06875
    return freq


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
