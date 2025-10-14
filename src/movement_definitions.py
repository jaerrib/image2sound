movement_type = {
    "sonata": {
        "phrases": [
            {"label": "A", "length": 16},
            {"label": "B", "length": 12},
            {"label": "C", "length": 6},
            {"label": "D", "length": 12},
            {"label": "E", "length": 8},
            {"label": "F", "length": 6},
            {"label": "G", "length": 12},
            {"label": "H", "length": 12},
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
            {"label": "D", "length": 11},
            {"label": "E", "length": 9},
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
            {"label": "Rondo Form", "sequence": ["A", "B", "A", "C", "A", "D", "A"]}
        ],
    },
    "finale": {
        "phrases": [
            {"label": "A", "length": 4},
            {"label": "B", "length": 6},
            {"label": "C", "length": 6},
            {"label": "D", "length": 4},
            {"label": "E", "length": 4},
            {"label": "F", "length": 2},
            {"label": "G", "length": 4},
            {"label": "H", "length": 4},
        ],
        "sections": [
            {"label": "Exposition", "sequence": ["A", "B", "A"]},
            {"label": "Development", "sequence": ["C", "D", "A"]},
            {"label": "Recapitulation", "sequence": ["E", "A", "F", "G"]},
            {"label": "Coda", "sequence": ["H"]},
        ],
    },
    "passacaglia": {
        "phrases": [
            {"label": "Ground", "length": 8},
            {"label": "Var1", "length": 8},
            {"label": "Var2", "length": 8},
            {"label": "Var3", "length": 8},
            {"label": "Var4", "length": 8},
            {"label": "Var5", "length": 8},
        ],
        "sections": [
            {"label": "Theme", "sequence": ["Ground"]},
            {
                "label": "Variations",
                "sequence": ["Var1", "Var2", "Var3", "Var4", "Var5", "Ground"],
            },
        ],
    },
    "chaconne": {
        "phrases": [
            {"label": "Bass", "length": 4},
            {"label": "VarA", "length": 8},
            {"label": "VarB", "length": 8},
            {"label": "VarC", "length": 8},
            {"label": "VarD", "length": 8},
        ],
        "sections": [
            {"label": "Theme", "sequence": ["Bass"]},
            {
                "label": "Variations",
                "sequence": ["VarA", "VarB", "VarC", "VarD", "Bass"],
            },
        ],
    },
    "fugue": {
        "phrases": [
            {"label": "Subject", "length": 4},
            {"label": "Answer", "length": 4},
            {"label": "Countersubject", "length": 4},
            {"label": "Episode", "length": 10},
            {"label": "Stretto", "length": 6},
            {"label": "Coda", "length": 4},
        ],
        "sections": [
            {
                "label": "Exposition",
                "sequence": ["Subject", "Answer", "Countersubject"],
            },
            {
                "label": "Middle Entries",
                "sequence": ["Episode", "Subject", "Episode", "Answer"],
            },
            {"label": "Final Section", "sequence": ["Stretto", "Subject", "Coda"]},
        ],
    },
    "nocturne": {
        "phrases": [
            {"label": "A", "length": 12},
            {"label": "B", "length": 16},
            {"label": "A'", "length": 12},
        ],
        "sections": [
            {"label": "Opening", "sequence": ["A"]},
            {"label": "Middle", "sequence": ["B"]},
            {"label": "Return", "sequence": ["A'"]},
        ],
    },
    "toccata": {
        "phrases": [
            {"label": "Flourish1", "length": 2},
            {"label": "A", "length": 4},
            {"label": "B", "length": 6},
            {"label": "Flourish2", "length": 2},
            {"label": "C", "length": 4},
            {"label": "D", "length": 6},
            {"label": "E", "length": 8},
        ],
        "sections": [
            {"label": "Opening", "sequence": ["Flourish1", "A", "B"]},
            {"label": "Middle", "sequence": ["Flourish2", "C", "D"]},
            {"label": "Climax", "sequence": ["E", "A", "B", "E"]},
        ],
    },
    "lament": {
        "phrases": [
            {"label": "A", "length": 8},
            {"label": "B", "length": 8},
            {"label": "C", "length": 10},
        ],
        "sections": [
            {"label": "Statement", "sequence": ["A"]},
            {"label": "Expansion", "sequence": ["B"]},
            {"label": "Climax/Resolution", "sequence": ["C"]},
        ],
    },
    "prelude": {
        "phrases": [
            {"label": "Intro", "length": 6},
            {"label": "Figuration1", "length": 8},
            {"label": "Figuration2", "length": 8},
            {"label": "Climax", "length": 10},
            {"label": "Coda", "length": 4},
        ],
        "sections": [
            {"label": "Opening", "sequence": ["Intro"]},
            {
                "label": "Developmental Passage",
                "sequence": ["Figuration1", "Figuration2"],
            },
            {"label": "Climax", "sequence": ["Climax"]},
            {"label": "Closing", "sequence": ["Coda"]},
        ],
    },
    "theme_and_variations": {
        "phrases": [
            {"label": "A", "length": 8},
            {"label": "B", "length": 8},
            {"label": "C", "length": 8},
            {"label": "D", "length": 8},
            {"label": "E", "length": 8},
            {"label": "F", "length": 8},
        ],
        "sections": [
            {"label": "Theme Statement", "sequence": ["A"]},
            {"label": "Variation Cycle", "sequence": ["B", "C", "D", "E", "F"]},
        ],
    },
    "concerto_ritornello": {
        "phrases": [
            {"label": "A", "length": 12},
            {"label": "B", "length": 8},
            {"label": "C", "length": 10},
            {"label": "D", "length": 8},
            {"label": "E", "length": 12},
        ],
        "sections": [
            {"label": "Opening Section", "sequence": ["A"]},
            {"label": "Middle Cycle 1", "sequence": ["B", "A"]},
            {"label": "Middle Cycle 2", "sequence": ["C", "A"]},
            {"label": "Middle Cycle 3", "sequence": ["D"]},
            {"label": "Closing Section", "sequence": ["E"]},
        ],
    },
    "french_overture": {
        "phrases": [
            {"label": "A", "length": 10},
            {"label": "B", "length": 16},
            {"label": "C", "length": 6},
        ],
        "sections": [
            {"label": "Grave Introduction", "sequence": ["A"]},
            {"label": "Fugal Allegro", "sequence": ["B"]},
            {"label": "Closing", "sequence": ["C"]},
        ],
    },
    "allemande": {
        "phrases": [{"label": "A", "length": 8}, {"label": "B", "length": 8}],
        "sections": [
            {"label": "Binary Form with Repeats", "sequence": ["A", "A", "B", "B"]}
        ],
    },
    "courante": {
        "phrases": [{"label": "A", "length": 10}, {"label": "B", "length": 10}],
        "sections": [
            {"label": "Binary Form with Repeats", "sequence": ["A", "A", "B", "B"]}
        ],
    },
    "sarabande": {
        "phrases": [{"label": "A", "length": 8}, {"label": "B", "length": 8}],
        "sections": [
            {"label": "Binary Form with Repeats", "sequence": ["A", "A", "B", "B"]}
        ],
    },
    "gigue": {
        "phrases": [{"label": "A", "length": 12}, {"label": "B", "length": 12}],
        "sections": [
            {"label": "Binary Form with Repeats", "sequence": ["A", "A", "B", "B"]}
        ],
    },
    "minuet": {
        "phrases": [
            {"label": "A", "length": 8},
            {"label": "B", "length": 8},
            {"label": "C", "length": 8},
            {"label": "D", "length": 8},
        ],
        "sections": [
            {"label": "Minuet I", "sequence": ["A", "B"]},
            {"label": "Trio", "sequence": ["C", "D"]},
            {"label": "Minuet I da capo", "sequence": ["A", "B"]},
        ],
    },
    "gavotte": {
        "phrases": [{"label": "A", "length": 8}, {"label": "B", "length": 8}],
        "sections": [
            {"label": "Binary Form with Repeats", "sequence": ["A", "A", "B", "B"]}
        ],
    },
    "bourree": {
        "phrases": [{"label": "A", "length": 8}, {"label": "B", "length": 8}],
        "sections": [
            {"label": "Binary Form with Repeats", "sequence": ["A", "A", "B", "B"]}
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
