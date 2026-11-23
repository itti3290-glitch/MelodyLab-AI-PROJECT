import json
from dotenv import load_dotenv
from google import genai
from langgraph.types import interrupt
from mido import (
    MidiFile,
    MidiTrack,
    Message,
    MetaMessage,
    bpm2tempo
)

from state import MelodyState
load_dotenv()
NOTE_MAP = {
    "C4": 60,
    "D4": 62,
    "E4": 64,
    "F4": 65,
    "G4": 67,
    "A4": 69,
    "B4": 71
}


def generate_melody(state: MelodyState):
    """
    Uses Gemini to generate an original melody
    containing exactly 8 supported musical notes.
    """
    client = genai.Client()
    try:
        response = client.models.generate_content(
           model="gemini-3.5-flash-lite",
            contents=f"""
            Create an original short melody.
            User request: {state['user_request']}
            Instrument: {state['instrument']}
            Mood: {state['mood']}
            Tempo: {state['tempo']}

            Generate exactly 8 musical notes.
            Use only these notes:
            C4, D4, E4, F4, G4, A4, B4.
            Return only the melody as JSON.
            """,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": {
                    "type": "OBJECT",
                    "properties": {
                        "melody": {
                            "type": "ARRAY",
                            "items": {
                                "type": "STRING"
                            },
                            "minItems": 8,
                            "maxItems": 8
                        }
                    },
                    "required": ["melody"]
                }
            }
        )

        melody_data = json.loads(response.text)
        melody = melody_data["melody"]

        # Validate melody length
        if len(melody) != 8:
            raise ValueError(
                "Gemini must generate exactly 8 notes"
            )

        # Validate supported notes
        if any(note not in NOTE_MAP for note in melody):
            raise ValueError(
                "Gemini returned an unsupported musical note"
            )

        return {
            "melody": melody,
            "revision_count": 0
        }

    finally:
        client.close()


def approve_melody(state: MelodyState):
    """
    Pauses the graph and asks the user to approve the melody.
    """

    answer = interrupt({
        "message": "האם לאשר את המנגינה?",
        "melody": state["melody"]
    })

    return {
        "approval": answer
    }


def route_after_approval(state: MelodyState):
    """
    Decides what happens after human approval.
    """

    if state["approval"]:
        return "create_midi"

    if state["revision_count"] < 1:
        return "revise_melody"

    return "stop"


def revise_melody(state: MelodyState):
    """
    Performs a local revision without another Gemini API call.
    """

    melody = state["melody"].copy()

    if melody[-1] == "A4":
        melody[-1] = "G4"
    else:
        melody[-1] = "A4"

    return {
        "melody": melody,
        "revision_count": state["revision_count"] + 1
    }


def create_midi(state: MelodyState):
    """
    Converts the generated melody into a MIDI file.
    """

    midi = MidiFile()
    track = MidiTrack()

    midi.tracks.append(track)

    # Set tempo before the notes
    track.append(
        MetaMessage(
            "set_tempo",
            tempo=bpm2tempo(state["tempo"])
        )
    )

    # Set instrument
    track.append(
        Message("program_change", program=0)
    )

    # Add melody notes
    for note in state["melody"]:

        pitch = NOTE_MAP[note]

        track.append(
            Message(
                "note_on",
                note=pitch,
                velocity=64,
                time=0
            )
        )

        track.append(
            Message(
                "note_off",
                note=pitch,
                velocity=64,
                time=480
            )
        )

    midi.save("melody.mid")

    print("MIDI file created: melody.mid")

    return {}