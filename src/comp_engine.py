NOTES_PER_MEASURE = 16

import movement_definitions


def generate_movement(movement_style: str, image_array):
    phrase_library: dict = generate_phrase_library(image_array, movement_style)
    movement: dict = {}
    for section in movement_definitions.movement_type[movement_style]["sections"]:
        label: str = section["label"]
        sequence: list = section["sequence"]
        section_data: list = generate_section_library(phrase_library, sequence)
        movement[label] = section_data
    return movement


def generate_phrase_library(image_array, movement_style: str):
    phrase_library: dict = {}
    note_index: int = 0  # Starting point for scanning image_array
    for phrase in movement_definitions.movement_type[movement_style]["phrases"]:
        label = phrase["label"]
        length = phrase["length"]
        phrase_data, note_index = generate_phrase(length, note_index, image_array)
        phrase_library[label] = phrase_data
    return phrase_library


def generate_section_library(phrase_library: dict, sequence: list):
    section: list = []
    for label in sequence:
        if label not in phrase_library:
            raise ValueError(f"Phrase '{label}' not found in phrase_library")
        section.append(phrase_library[label])
    return section


def generate_phrase(length: int, start_index: int, image_array):
    total_note_index: int = length * NOTES_PER_MEASURE
    phrase_array: list = []
    note_index: int = start_index
    num: int = 0
    while num < total_note_index:
        if note_index + 1 > len(image_array) - 1:
            note_index = len(image_array) - note_index
        comp_index: int = note_index + 1
        note_length: int = get_length(image_array[note_index], image_array[comp_index])
        if num + note_length > total_note_index:
            note_length = total_note_index - num
        phrase_array.append((image_array[note_index], note_length))
        num += note_length
        note_index += 1
    return phrase_array, note_index


def get_length(current_note: int, next_note: int):
    difference: int = abs(current_note - next_note)
    if difference <= 8:
        return 8  # Half note
    elif difference <= 16:
        return 4  # Quarter note
    elif difference <= 64:
        return 2  # Eighth note
    else:
        return 1  # Sixteenth note
