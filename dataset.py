
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()

dataset_name = "MelodyLab Evaluation"

dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="Test cases for evaluating MelodyLab"
)

examples = [
    {
        "inputs": {
            "user_request": "אני רוצה מנגינה מסתורית",
            "instrument": "piano",
            "mood": "mysterious",
            "tempo": 80
        },
        "reference_outputs": {
            "expected_mood": "mysterious"
        }
    },
    {
        "inputs": {
            "user_request": "אני רוצה מנגינה שמחה",
            "instrument": "piano",
            "mood": "happy",
            "tempo": 120
        },
        "reference_outputs": {
            "expected_mood": "happy"
        }
    },
    {
        "inputs": {
            "user_request": "אני רוצה מנגינה רגועה",
            "instrument": "piano",
            "mood": "calm",
            "tempo": 60
        },
        "reference_outputs": {
            "expected_mood": "calm"
        }
    }
]

client.create_examples(
    dataset_name=dataset_name,
    examples=examples
)

print("Dataset created successfully!")
