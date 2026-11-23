from dotenv import load_dotenv
from langsmith import evaluate

from nodes import generate_melody
from evaluator import evaluate_melody

load_dotenv()

dataset_name = "MelodyLab Evaluation"


def melody_generator(inputs):
    return generate_melody(inputs)


results = evaluate(
    melody_generator,
    data=dataset_name,
    evaluators=[evaluate_melody],
    experiment_prefix="MelodyLab - Improved"
)

print("Improved evaluation completed!")