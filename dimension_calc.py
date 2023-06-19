from math import sqrt, floor


def get_new_dim(img_dim, time_in_minutes, tempo):
    target_pixels = time_in_minutes * tempo
    img_ratio = img_dim[0] / img_dim[1]
    new_height = floor(sqrt(target_pixels / img_ratio))
    new_width = floor(new_height * img_ratio)
    return new_width, new_height
