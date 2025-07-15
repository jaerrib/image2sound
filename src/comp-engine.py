TEST_DATA = [
    16,
    128,
    5,
    200,
    78,
    42,
    0,
    0,
    231,
    79,
    42,
    60,
    126,
    100,
    7,
    46,
    82,
    46,
    87,
    13,
    90,
    45,
    72,
    128,
    201,
    199,
    244,
    100,
]
NOTES_PER_MEASURE = 16


def generate_section(start_index, phrase_setup, test_info):
    section = {}
    current_index = start_index
    num_phrases = len(phrase_setup)
    for num in range(num_phrases):
        phrase_length = phrase_setup[num]
        new_phrase, new_index = generate_phrase(phrase_length, current_index, test_info)
        section[str(num)] = new_phrase
        required_space = phrase_length * NOTES_PER_MEASURE
        current_index = (new_index + required_space) % len(test_info)
    return section


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
    if difference <= 64:
        return 1
    elif difference <= 128:
        return 2
    elif difference <= 192:
        return 4
    else:
        return 8


# This is pattern of phrase lengths that make up the section
section_definition = [
    4,
    8,
    8,
    8,
    8,
    4,
]

new_section = generate_section(
    start_index=0, phrase_setup=section_definition, test_info=TEST_DATA
)
print(new_section)
