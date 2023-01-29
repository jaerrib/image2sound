import numpy as np
from PIL import Image
from scipy.io import wavfile
from math import sqrt
import argparse


def get_channel_value(num):
    """
    Converts the numerical data taken from the WAV and converts it to a number
    between 0 and 255
    """
    channel_value = int(abs(num / 3871999.2109375))
    return channel_value


def get_color_array(file_path):
    """
    Accepts a path to a 24-bit WAV file, converts it to a numpy array, then
    subsequently converts the left channel to a red value, the right channel to
    a blue value, and the average of te left and right to green. Returns an
    array made up of the resulting RGB values.
    """
    output = wavfile.read(file_path)
    array = np.asarray(output[1])
    array_length = int(array.size / 2)
    temp_array = []
    for i in range(0, array_length):
        red = get_channel_value(array[i][0])
        green = get_channel_value((array[i][0] + array[i][1]) / 2)
        blue = get_channel_value(array[i][1])
        temp_array.append([red, green, blue])
    return temp_array


def make_sq_img(array):
    """
    Accepts the color array and rearranges it as a square image array
    """
    size = int(sqrt(len(array)))
    count = 0
    img_array = []
    for row_num in range(size):
        row = []
        for col_num in range(size):
            row.append([0, 0, 0])
        img_array.append(row)
    for j in range(size):
        for k in range(size):
            img_array[j][k] = array[count]
            count += 1
    return img_array


def save_wav(save_path, array):
    image = Image.fromarray(array.astype("uint8"), "RGB")
    maxsize = (1000, 1000)
    image.thumbnail(maxsize, Image.LANCZOS)
    split_str = save_path.split(".")
    split_str = split_str[0].split("/")
    file_name = split_str[-1]+".jpg"
    image.save(file_name)
    print("Saved file as ", file_name)


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str)
args = parser.parse_args()
path = args.path
color_array = get_color_array(path)
square_image = np.array(make_sq_img(color_array))
save_wav(path, square_image)
