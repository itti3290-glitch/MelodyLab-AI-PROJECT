from dotenv import load_dotenv
load_dotenv()

from graph import graph
from langgraph.types import Command


initial_state = {
    "user_request": "אני רוצה מנגינה מסתורית",
    "instrument": "piano",
    "mood": "mysterious",
    "tempo": 80
}

config = {
    "configurable": {
        "thread_id": "melody_001"
    }
}

result = graph.invoke(initial_state, config)

while result.get("__interrupt__"):
    print(result["__interrupt__"])

    answer = input("לאשר את המנגינה? (y/n): ").strip().lower()

    approval = answer == "y"

    result = graph.invoke(
        Command(resume=approval),
        config
    )

print("Final result:", result)