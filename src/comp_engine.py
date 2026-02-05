NOTES_PER_MEASURE = 16

import movement_definitions


def generate_movement(movement_style: str, image_array, avg_color_dif: float):
    phrase_library: dict = generate_phrase_library(
        image_array, movement_style, avg_color_dif
    )
    movement: dict = {}
    for section in movement_definitions.movement_type[movement_style]["sections"]:
        label: str = section["label"]
        sequence: list = section["sequence"]
        section_data: list = generate_section_library(phrase_library, sequence)
        movement[label] = section_data
    return movement


def generate_phrase_library(image_array, movement_style: str, avg_color_dif: float):
    phrase_library: dict = {}
    note_index: int = 0  # Starting point for scanning image_array
    for phrase in movement_definitions.movement_type[movement_style]["phrases"]:
        label = phrase["label"]
        length = phrase["length"]
        phrase_data, note_index = generate_phrase(
            length, note_index, image_array, avg_color_dif
        )
        phrase_library[label] = phrase_data
    return phrase_library


def generate_section_library(phrase_library: dict, sequence: list):
    section: list = []
    for label in sequence:
        if label not in phrase_library:
            raise ValueError(f"Phrase '{label}' not found in phrase_library")
        section.append(phrase_library[label])
    return section


def generate_phrase(length: int, start_index: int, image_array, avg_color_dif: float):
    total_notes: int = length * NOTES_PER_MEASURE
    phrase: list = []
    note_index: int = start_index
    count: int = 0
    while count < total_notes:
        current: int = image_array[note_index]
        next_val: int = image_array[(note_index + 1) % len(image_array)]
        note_length = get_length(current, next_val, avg_color_dif)
        if count + note_length > total_notes:
            note_length = total_notes - count
        phrase.append((current, note_length))
        count += note_length
        note_index = (note_index + 1) % len(image_array)
    return phrase, note_index


def get_length(current_note: int, next_note: int, avg_color_dif: float):
    difference: int = abs(current_note - next_note)
    modifier: float = avg_color_dif / 255  # Normalize the color difference to 0–1 range
    if difference <= 4 * modifier:
        return 8  # Half note
    elif difference <= 12 * modifier:
        return 4  # Quarter note
    elif difference <= 32 * modifier:
        return 2  # Eighth note
    else:
        return 1  # Sixteenth note`
