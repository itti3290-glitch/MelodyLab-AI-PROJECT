from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver

from nodes import (
    generate_melody,
    approve_melody,
    revise_melody,
    route_after_approval,
    create_midi
)

from state import MelodyState


builder = StateGraph(MelodyState)

# Register nodes
builder.add_node("generate_melody", generate_melody)
builder.add_node("approve_melody", approve_melody)
builder.add_node("revise_melody", revise_melody)
builder.add_node("create_midi", create_midi)

# Define workflow
builder.add_edge(START, "generate_melody")

builder.add_edge("generate_melody", "approve_melody")
builder.add_edge("revise_melody", "approve_melody")
builder.add_edge("create_midi", END)

# Conditional routing after human approval
builder.add_conditional_edges(
    "approve_melody",
    route_after_approval,
    {
        "create_midi": "create_midi",
        "revise_melody": "revise_melody",
        "stop": END
    }
)

# Memory for Human-in-the-Loop
memory = InMemorySaver()

graph = builder.compile(checkpointer=memory)