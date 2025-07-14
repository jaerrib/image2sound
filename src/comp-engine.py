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
    print(num)
    return phrase_array


def get_length(current_note, next_note):
    difference = abs(current_note - next_note)
    if 0 <= difference <= 64:
        return 1
    elif 65 <= difference <= 128:
        return 2
    elif 129 <= difference <= 1250:
        return 4
    else:
        return 8


phrase: list[tuple[float, int]] = generate_phrase(
    length=8, start_index=0, test_info=TEST_DATA
)
print(phrase)
