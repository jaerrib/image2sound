FREQ_DICT = {
    "A0": 27.5000,
    "A#0": 29.13524,
    "B0": 30.86771,

    "C1": 32.70320,
    "C#1": 34.64783,
    "D1": 36.70810,
    "D#1": 38.89087,
    "E1": 41.20344,
    "F1": 43.65353,
    "F#1": 46.24930,
    "G1": 48.99943,
    "G#1": 51.91309,
    "A1": 55.00000,
    "A#1": 58.27047,
    "B1": 61.73541,

    "C2": 65.40639,
    "C#2": 69.29566,
    "D2": 73.41619,
    "D#2": 77.78175,
    "E2": 82.40689,
    "F2": 87.30706,
    "F#2": 92.49861,
    "G2": 97.49861,
    "G#2": 103.8262,
    "A2": 110.0000,
    "A#2": 116.5409,
    "B2": 123.4708,

    "C3": 130.8128,
    "C#3": 138.5913,
    "D3": 146.8324,
    "D#3": 155.5635,
    "E3": 164.8138,
    "F3": 174.6141,
    "F#3": 184.9972,
    "G3": 195.9977,
    "G#3": 207.6523,
    "A3": 220.0000,
    "A#3": 233.0819,
    "B3": 246.9417,

    "C4": 261.6256,
    "C#4": 277.1826,
    "D4": 293.6646,
    "D#4": 311.1270,
    "E4": 329.6276,
    "F4": 349.2282,
    "F#4": 369.9944,
    "G4": 391.9954,
    "G#4": 415.3047,
    "A4": 440.0000,
    "A#4": 466.1638,
    "B4": 493.8833,

    "C5": 523.2511,
    "C#5": 523.2511,
    "D5": 587.3295,
    "D#5": 622.2540,
    "E5": 659.4565,
    "F5": 698.4565,
    "F#5": 739.9888,
    "G5": 783.9909,
    "G#5": 830.6094,
    "A5": 880.0000,
    "A#5": 932.3275,
    "B5": 987.7666,

    "C6": 1046.502,
    "C#6": 1108.731,
    "D6": 1174.659,
    "D#6": 1244.508,
    "E6": 1318.510,
    "F6": 1396.913,
    "F#6": 1479.978,
    "G6": 1567.982,
    "G#6": 1661.219,
    "A6": 1760.000,
    "A#6": 1864.655,
    "B6": 1975.533,

    "C7": 2093.005,
    "C#7": 2217.461,
    "D7": 2349.318,
    "D#7": 248.016,
    "E7": 2637.020,
    "F7": 2793.826,
    "F#7": 2969.955,
    "G7": 3135.963,
    "G#7": 3322.438,
    "A7": 3520.000,
    "A#7": 3729.310,
    "B7": 3951.066,

    "C8": 4186.009,
}

SCALE = {
    # Major keys
    "CMajor": ["C", "D", "E", "F", "G", "A", "B"],
    "C#Major": ["C#", "D#", "F", "F#", "G#", "A#", "B#"],
    "DbMajor": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "DMajor": ["D", "E", "F#", "G", "A", "B", "C#"],
    "D#Major": ["D#", "E#", "F##", "G#", "A#", "B#", "C##"],
    "EbMajor": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    "EMajor": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "FMajor": ["F", "G", "A", "Bb", "C", "D", "E"],
    "F#Major": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "GbMajor": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
    "GMajor": ["G", "A", "B", "C", "D", "E", "F#"],
    "G#Major": ["G#", "A#", "B#", "C#", "D#", "E#", "F##"],
    "AbMajor": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "AMajor": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "A#Major": ["A#", "B#", "C##", "D#", "E#", "F##", "G##"],
    "BbMajor": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "BMajor": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    "CbMajor": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],

    # Minor keys
    "CMinor": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
    "C#Minor": ["C#", "D#", "E", "F#", "G#", "A", "B"],
    "DMinor": ["D", "E", "F", "G", "A", "Bb", "C"],
    "D#Minor": ["D#", "E#", "F#", "G#", "A#", "B", "C#"],
    "EbMinor": ["Eb", "F", "Gb", "Ab", "Bb", "Cb", "Db"],
    "EMinor": ["E", "F#", "G", "A", "B", "C", "D"],
    "FMinor": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
    "F#Minor": ["F#", "G#", "A", "B", "C#", "D", "E"],
    "GMinor": ["G", "A", "Bb", "C", "D", "Eb", "F"],
    "G#Minor": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
    "AMinor": ["A", "B", "C", "D", "E", "F", "G"],
    "A#Minor": ["A#", "B#", "C#", "D#", "E#", "F#", "G#"],
    "BbMinor": ["Bb", "C", "Db", "Eb", "F", "Gb", "Ab"],
    "BMinor": ["B", "C#", "D", "E", "F#", "G", "A"],

    # Major Pentatonic
    "CMajorPentatonic": ["C", "D", "E", "G", "A"],
    "C#MajorPentatonic": ["C#", "D#", "F", "G#", "A#"],
    "DbMajorPentatonic": ["Db", "Eb", "F", "Ab", "Bb"],
    "DMajorPentatonic": ["D", "E", "F#", "A", "B"],
    "D#MajorPentatonic": ["D#", "F", "G#", "A#", "C"],
    "EbMajorPentatonic": ["Eb", "F", "G", "Bb", "C"],
    "EMajorPentatonic": ["E", "F#", "G#", "B", "C#"],
    "FMajorPentatonic": ["F", "G", "A", "C", "D"],
    "F#MajorPentatonic": ["F#", "G#", "A#", "C#", "D#"],
    "GbMajorPentatonic": ["Gb", "Ab", "Bb", "Db", "Eb"],
    "GMajorPentatonic": ["G", "A", "B", "D", "E"],
    "G#MajorPentatonic": ["G#", "A#", "C", "D#", "F"],
    "AbMajorPentatonic": ["Ab", "Bb", "C", "Eb", "F"],
    "AMajorPentatonic": ["A", "B", "C#", "E", "F#"],
    "A#MajorPentatonic": ["A#", "B#", "D", "F", "G"],
    "BbMajorPentatonic": ["Bb", "C", "D", "F", "G"],
    "BMajorPentatonic": ["B", "C#", "D#", "F#", "G#"],

    # Minor Pentatonic
    "CMinorPentatonic": ["C", "Eb", "F", "G", "Bb"],
    "C#MinorPentatonic": ["C#", "E", "F#", "G#", "B"],
    "DMinorPentatonic": ["D", "F", "G", "A", "C"],
    "D#MinorPentaonic": ["D#", "F#", "G#", "A#", "C#"],
    "EbMinorPentatonic": ["Eb", "Gb", "Ab", "Bb", "Db"],
    "EMinorPentatonic": ["E", "G", "A", "B", "D"],
    "FMinorPentatonic": ["F", "Ab", "Bb", "C", "Eb"],
    "F#MinorPentaonic": ["F#", "A", "B", "C#", "E"],
    "GbMinorPentatonic": ["G", "A", "B", "Db", "E"],
    "GMinorPentatonic": ["G", "Bb", "C", "D", "F"],
    "G#MinorPentaonic": ["G#", "B", "C#", "D#", "F#"],
    "AMinorPentatonic": ["A", "C", "D", "E", "G"],
    "A#MinorPentatonic": ["A#", "C#", "D#", "E#", "G#"],
    "BbMinorPentatonic": ["Bb", "Db", "Eb", "F", "Ab"],
    "BMinorPentatonic": ["B", "D", "E", "F#", "A"],

    # Chromatic
    "chromatic": [
        "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
    ]
}

EQUIVALENT_NOTES = {
    "Cb": "B",
    "Db": "C#",
    "Eb": "D#",
    "E#": "F",
    "Fb": "E",
    "Gb": "F#",
    "Ab": "G#",
    "Bb": "A#",
    "B#": "C",
    "C##": "D",
    "F##": "G",
    "G##": "A"
}


def flat_conversion(scale):
    for index in range(len(scale)):
        if scale[index] in EQUIVALENT_NOTES:
            note = scale[index]
            scale[index] = EQUIVALENT_NOTES[note]
    return scale


def get_tone_array(key):
    scale_array = flat_conversion(SCALE[key])
    tone_array = []
    for index in range(1, 8):
        for note in scale_array:
            tone_array.append(FREQ_DICT[note+str(index)])
    return tone_array


def get_chromatic_notes():
    return SCALE["chromatic"]
