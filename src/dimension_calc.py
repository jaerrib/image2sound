import math


def get_new_dim(img_dim, time_in_minutes, tempo, time_signature):
    img_ratio = img_dim[0] / img_dim[1]
    notes_per_minute = tempo * time_signature[1]
    new_height = math.floor(math.sqrt(time_in_minutes * notes_per_minute / img_ratio))
    new_width = math.floor(new_height * img_ratio)
    return new_width, new_height
