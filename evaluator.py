ALLOWED_NOTES = {"C4", "D4", "E4", "F4", "G4", "A4", "B4"}


def evaluate_melody(inputs, outputs, reference_outputs):
    melody = outputs.get("melody", [])

    is_valid = (
        isinstance(melody, list)
        and len(melody) == 8
        and all(note in ALLOWED_NOTES for note in melody)
    )

    return {
        "key": "melody_validity",
        "score": 1 if is_valid else 0
    }