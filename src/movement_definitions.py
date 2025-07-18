movement_type = {
    "sonata": {
        "phrases": [
            {"label": "A", "length": 8},
            {"label": "B", "length": 8},
            {"label": "C", "length": 6},
            {"label": "D", "length": 8},
            {"label": "E", "length": 8},
            {"label": "F", "length": 6},
            {"label": "G", "length": 8},
            {"label": "H", "length": 8},
            {"label": "I", "length": 4},
            {"label": "J", "length": 4},
        ],
        "sections": [
            {"label": "Exposition", "sequence": ["A", "B", "C", "D"]},
            {"label": "Development", "sequence": ["E", "F", "C", "F", "E"]},
            {"label": "Recapitulation", "sequence": ["G", "H", "C", "D"]},
            {"label": "Coda", "sequence": ["I", "J"]},
        ],
    },
    "adagio": {
        "phrases": [
            {"label": "A", "length": 10},
            {"label": "B", "length": 10},
            {"label": "C", "length": 12},
            {"label": "D", "length": 10},
            {"label": "E", "length": 10},
        ],
        "sections": [
            {"label": "A Section", "sequence": ["A", "B"]},
            {"label": "B Section", "sequence": ["C"]},
            {"label": "A' Section", "sequence": ["D", "E"]},
        ],
    },
    "scherzo": {
        "phrases": [
            {"label": "A", "length": 8},
            {"label": "B", "length": 8},
            {"label": "C", "length": 6},
            {"label": "D", "length": 6},
        ],
        "sections": [
            {"label": "Scherzo", "sequence": ["A", "B"]},
            {"label": "Trio", "sequence": ["C", "D"]},
            {"label": "Scherzo da capo", "sequence": ["A", "B"]},
        ],
    },
    "rondo": {
        "phrases": [
            {"label": "A", "length": 6},
            {"label": "B", "length": 10},
            {"label": "C", "length": 10},
            {"label": "D", "length": 8},
        ],
        "sections": [
            {"label": "Rondo Form", "sequence": ["A", "B", "A", "C", "A", "D"]}
        ],
    },
    "punk": {
        "phrases": [
            {"label": "A", "length": 4},
            {"label": "B", "length": 8},
            {"label": "C", "length": 8},
            {"label": "D", "length": 2},
        ],
        "sections": [
            {"label": "Intro", "sequence": ["A", "A"]},
            {"label": "Verse Cycle", "sequence": ["B", "C", "B", "C", "B", "C"]},
            {"label": "Outro", "sequence": ["D"]},
        ],
    },
}
