from typing import TypedDict, NotRequired


class MelodyState(TypedDict):
    user_request: str
    instrument: str
    mood: str
    tempo: int

    melody: NotRequired[list[str]]
    approval: NotRequired[bool]
    revision_count: NotRequired[int]