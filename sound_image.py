from PIL import Image
import numpy as np
import wavio
from math import trunc


class SoundImage:

    def __init__(self, path, key="C"):
        self.path = path
        self.key = key
        self.image_array = self.image_to_array(path)

    @staticmethod
    def image_to_array(path):
        img = Image.open(path).convert(mode="RGB")
        img_arr = np.asarray(img, dtype='int64')
        return img_arr

    @staticmethod
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

    def get_sin(self, color):
        freq = self.get_freq(color)
        rate = 44100
        time = .75
        n = int(rate * time)
        time_grid = np.arange(n) / rate
        return np.sin(2 * np.pi * freq * time_grid)

    @staticmethod
    def save_wav(save_path, side, array):
        rate = 44100
        split_str = save_path.split(".")
        split_str = split_str[0].split("/")
        file_name = split_str[-1] + side + ".wav"
        wavio.write(file_name, array, rate, scale=2, sampwidth=3, clip="ignore")
        print("Saved file as ", file_name)

    def convert_to_multiple(self):
        red_array = []
        green_array = []
        blue_array = []
        for x in self.image_array:
            for y in x:
                red = y[0]
                green = y[1]
                blue = y[2]
                red_value = self.get_sin(red)
                green_value = self.get_sin(green)
                blue_value = self.get_sin(blue)
                red_array.append([red_value])
                green_array.append([green_value])
                blue_array.append([blue_value])
        self.save_wav(self.path, "-R", red_array)
        self.save_wav(self.path, "-G", green_array)
        self.save_wav(self.path, "-B", blue_array)
