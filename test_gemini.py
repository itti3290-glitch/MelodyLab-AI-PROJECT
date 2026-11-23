
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="""
    Create a short mysterious piano melody.
    Use only these notes: C4, D4, E4, F4, G4, A4, B4.
    Choose a tempo between 60 and 140.
    Return exactly 8 notes.
    """,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": {
            "type": "OBJECT",
            "properties": {
                "mood": {"type": "STRING"},
                "tempo": {"type": "INTEGER"},
                "melody": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"}
                }
            },
            "required": ["mood", "tempo", "melody"]
        }
    }
)

melody_data = json.loads(response.text)

print("Generated melody:")
print(melody_data)

client.close()

