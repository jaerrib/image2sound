NOTES_PER_MEASURE = 16


def generate_movement(movement_info, test_info):
    movement = {}
    current_index = 0
    section_library = {}
    for num, entry in enumerate(movement_info):
        section_label = entry["section"]
        section_definition = entry["definition"]
        if section_label in section_library:
            new_section = section_library[section_label]
        else:
            new_section, new_index = generate_section(
                current_index, section_definition, test_info
            )
            section_library[section_label] = new_section
            current_index = new_index % len(test_info)
        movement[str(num)] = new_section
    return movement


def generate_section(start_index, phrase_setup, test_info):
    section = {}
    current_index = start_index
    phrase_library = {}
    for num, entry in enumerate(phrase_setup):
        label = entry["label"]
        length = entry["length"]
        if label in phrase_library:
            new_phrase = phrase_library[label]
        else:
            new_phrase, new_index = generate_phrase(length, current_index, test_info)
            phrase_library[label] = new_phrase
            required_space = length * NOTES_PER_MEASURE
            current_index = (new_index + required_space) % len(test_info)
        section[str(num)] = new_phrase
    return section, current_index


def generate_phrase(length, start_index, test_info):
    total_note_index = length * NOTES_PER_MEASURE
    phrase_array = []
    note_index = start_index
    num = 0
    while num < total_note_index:
        if note_index + 1 > len(test_info) - 1:
            note_index = len(test_info) - note_index
        comp_index = note_index + 1
        note_length = get_length(test_info[note_index], test_info[comp_index])
        if num + note_length > total_note_index:
            note_length = total_note_index - num
        phrase_array.append((test_info[note_index], note_length))
        num += note_length
        note_index += 1
    return phrase_array, note_index


def get_length(current_note, next_note):
    difference = abs(current_note - next_note)
    if difference <= 8:
        return 8  # Half note
    elif difference <= 16:
        return 4  # Quarter note
    elif difference <= 64:
        return 2  # Eighth note
    else:
        return 1  # Sixteenth note


# Example movement made up of three sections
movement_definition = [
    {
        "section": 1,
        "definition": [
            {"label": "A", "length": 8},
            {"label": "B", "length": 8},
            {"label": "C", "length": 8},
            {"label": "D", "length": 8},
        ],
    },
    {
        "section": 2,
        "definition": [
            {"label": "A", "length": 8},
            {"label": "A", "length": 8},
            {"label": "A", "length": 8},
            {"label": "A", "length": 8},
        ],
    },
    {
        "section": 3,
        "definition": [
            {"label": "A", "length": 8},
            {"label": "B", "length": 8},
            {"label": "C", "length": 8},
            {"label": "D", "length": 8},
        ],
    },
    {
        "section": 4,
        "definition": [
            {"label": "A", "length": 4},
            {"label": "B", "length": 4},
            {"label": "C", "length": 4},
            {"label": "D", "length": 4},
        ],
    },
]
