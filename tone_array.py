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
    "C": ["C", "D", "E", "F", "G", "A", "B"],
    "C#": ["C#", "D#", "F", "F#", "G#", "A#", "B#"],
    "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#"],
    "D#": ["D#", "E#", "F##", "G#", "A#", "B#", "C##"],
    "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "F": ["F", "G", "A", "Bb", "C", "D", "E"],
    "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
    "G": ["G", "A", "B", "C", "D", "E", "F#"],
    "G#": ["G#", "A#", "B#", "C#", "D#", "E#", "F##"],
    "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "A#": ["A#", "B#", "C##", "D#", "E#", "F##", "G##"],
    "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    "Cb": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],

    # Minor keys
    "Cminor": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
    "C#minor": ["C#", "D#", "E", "F#", "G#", "A", "B"],
    "Dminor": ["D", "E", "F", "G", "A", "Bb", "C"],
    "D#minor": ["D#", "E#", "F#", "G#", "A#", "B", "C#"],
    "Ebminor": ["Eb", "F", "Gb", "Ab", "Bb", "Cb", "Db"],
    "Eminor": ["E", "F#", "G", "A", "B", "C", "D"],
    "Fminor": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"],
    "F#minor": ["F#", "G#", "A", "B", "C#", "D", "E"],
    "Gminor": ["G", "A", "Bb", "C", "D", "Eb", "F"],
    "G#minor": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
    "Aminor": ["A", "B", "C", "D", "E", "F", "G"],
    "A#minor": ["A#", "B#", "C#", "D#", "E#", "F#", "G#"],
    "Bbminor": ["Bb", "C", "Db", "Eb", "F", "Gb", "Ab"],
    "Bminor": ["B", "C#", "D", "E", "F#", "G", "A"],

    # Major Pentatonic
    "Cpentatonic": ["C", "D", "E", "G", "A"],
    "C#pentatonic": ["C#", "D#", "F", "G#", "A#"],
    "Dbpentatonic": ["Db", "Eb", "F", "Ab", "Bb"],
    "Dpentatonic": ["D", "E", "F#", "A", "B"],
    "D#pentatonic": ["D#", "F", "G#", "A#", "C"],
    "Ebpentatonic": ["Eb", "F", "G", "Bb", "C"],
    "Epentatonic": ["E", "F#", "G#", "B", "C#"],
    "Fpentatonic": ["F", "G", "A", "C", "D"],
    "F#pentatonic": ["F#", "G#", "A#", "C#", "D#"],
    "Gbpentatonic": ["Gb", "Ab", "Bb", "Db", "Eb"],
    "Gpentatonic": ["G", "A", "B", "D", "E"],
    "G#pentatonic": ["G#", "A#", "C", "D#", "F"],
    "Abpentatonic": ["Ab", "Bb", "C", "Eb", "F"],
    "Apentatonic": ["A", "B", "C#", "E", "F#"],
    "A#pentatonic": ["A#", "B#", "D", "F", "G"],
    "Bbpentatonic": ["Bb", "C", "D", "F", "G"],
    "Bpentatonic": ["B", "C#", "D#", "F#", "G#"],

    # Minor Pentatonic
    "CminorPentatonic": ["C", "Eb", "F", "G", "Bb"],
    "C#minorPentatonic": ["C#", "E", "F#", "G#", "B"],
    "DminorPentatonic": ["D", "F", "G", "A", "C"],
    "D#minorPentaonic": ["D#", "F#", "G#", "A#", "C#"],
    "EbminorPentaonic": ["Eb", "Gb", "Ab", "Bb", "Db"],
    "EminorPentatonic": ["E", "G", "A", "B", "D"],
    "FminorPentatonic": ["F", "Ab", "Bb", "C", "Eb"],
    "F#minorPentaonic": ["F#", "A", "B", "C#", "E"],
    "GbminorPentatonic": ["G", "A", "B", "Db", "E"],
    "GminorPentatonic": ["G", "Bb", "C", "D", "F"],
    "G#minorPentaonic": ["G#", "B", "C#", "D#", "F#"],
    "AminorPentatonic": ["A", "C", "D", "E", "G"],
    "A#minorPentatonic": ["A#", "C#", "D#", "E#", "G#"],
    "BbminorPentatonic": ["Bb", "Db", "Eb", "F", "Ab"],
    "BminorPentatonic": ["B", "D", "E", "F#", "A"],
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
    print("Original scale", scale)
    for index in range(len(scale)):
        if scale[index] in EQUIVALENT_NOTES:
            note = scale[index]
            scale[index] = EQUIVALENT_NOTES[note]
    print("New scale", scale)
    return scale


def get_tone_array(key):
    scale_array = flat_conversion(SCALE[key])
    tone_array = []
    for index in range(1, 8):
        for note in scale_array:
            tone_array.append(FREQ_DICT[note+str(index)])
    return tone_array
