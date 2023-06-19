from PIL import Image
import numpy as np
import wavio
from math import trunc
from tone_array import get_tone_array
from dimension_calc import get_new_dim


class SoundImage:

    def __init__(self,
                 path,
                 key,
                 tempo,
                 minutes,
                 seconds,
                 split):
        self.path = path
        self.freq_dict = get_tone_array(key)
        self.length = len(self.freq_dict)
        self.tempo = tempo
        self.minutes = minutes
        self.seconds = seconds
        self.image_array = self.image_to_array(path,
                                               self.minutes,
                                               self.seconds,
                                               self.tempo)
        self.split = split

    @staticmethod
    def image_to_array(path, minutes, seconds, tempo):
        img = Image.open(path).convert(mode="RGB")
        img_dim = img.size
        size = get_new_dim(img_dim, minutes, seconds, tempo)
        output = img.resize(size)
        img_arr = np.asarray(output, dtype='int64')
        return img_arr

    def get_freq(self, color):
        divisor = 256 / self.length
        key_item = int(trunc(color / divisor))
        return self.freq_dict[key_item]

    def get_sin(self, color):
        freq = self.get_freq(color)
        rate = 44100
        time = 60 / self.tempo
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

    def convert_to_stereo(self):
        left_data = []
        right_data = []
        for x in self.image_array:
            for y in x:
                red = y[0]
                green = y[1]
                blue = y[2]
                left_value = self.get_sin((red + green) / 2)
                right_value = self.get_sin((blue + green) / 2)
                left_data.append(left_value)
                right_data.append(right_value)
        left = np.array(left_data)
        right = np.array(right_data)
        combined = np.hstack((left.reshape(-1, 1), right.reshape(-1, 1)))
        self.save_wav(self.path, "-stereo", combined)

    def convert(self):
        if not self.split:
            self.convert_to_stereo()
        else:
            self.convert_to_multiple()
