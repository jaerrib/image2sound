from PIL import Image
import numpy as np
import wavio
import argparse
from math import trunc


def image_to_array(save_path):
    img = Image.open(save_path).convert(mode="RGB")
    img_arr = np.asarray(img, dtype='int64')
    return img_arr


def get_freq(color):
    freq_dict = {
        "0": 130.8128,
        "1": 146.8324,
        "2": 164.8138,
        "3": 174.6141,
        "4": 195.9977,
        "5": 220.0000,
        "6": 246.9417,
        "7": 261.6256,
        "8": 293.6646,
        "9": 329.6276,
        "10": 349.2282,
        "11": 391.9954,
        "12": 440.0000,
        "13": 493.8833,
        "14": 523.2511,
        "15": 587.3295,
        "16": 659.4565,
        "17": 698.4565,
        "18": 783.9909,
        "19": 880.0000,
        "20": 987.7666,
        "21": 1046.502,
        "22": 1174.659,
        "23": 1318.510,
        "24": 1396.913,
        "25": 1567.982,
        "26": 1760.000,
        "27": 1975.533,
        "28": 2093.005,
        "29": 2349.318,
        "30": 2637.020,
        "31": 2793.826,
        "32": 3135.963,
        "33": 3520.000,
        "34": 3951.066,
    }
    key_item = str(trunc(color / 7.314285714))
    return freq_dict[key_item]


def get_sin(color):
    freq = get_freq(color)
    rate = 44100
    time = .75
    n = int(rate * time)
    time_grid = np.arange(n) / rate
    return np.sin(2 * np.pi * freq * time_grid)


def save_wav(save_path, side, array):
    rate = 44100
    split_str = save_path.split(".")
    split_str = split_str[0].split("/")
    file_name = split_str[-1]+side+".wav"
    wavio.write(file_name, array, rate, scale=2, sampwidth=3, clip="ignore")
    print("Saved file as ", file_name)


def convert_to_multiple(file_path):
    image_array = image_to_array(file_path)
    red_array = []
    green_array = []
    blue_array = []
    for x in image_array:
        for y in x:
            red = y[0]
            green = y[1]
            blue = y[2]
            red_value = get_sin(red)
            green_value = get_sin(green)
            blue_value = get_sin(blue)
            red_array.append([red_value])
            green_array.append([green_value])
            blue_array.append([blue_value])
    save_wav(file_path, "-R", red_array)
    save_wav(file_path, "-G", green_array)
    save_wav(file_path, "-B", blue_array)


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str)
args = parser.parse_args()
path = args.path

convert_to_multiple(path)
