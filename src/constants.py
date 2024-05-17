from models import Action

WAIT_MESSAGES = [
    "Reading minds...",
    "Generating hands...",
    "Thinking...",
    "Flipping a coin...",
    "Guessing the right move...",
    "Doing maths...",
    "Looking for checkmate...",
    "Picking up a draw four...",
    "Phoning a friend..."
]

RESPONSE_TO_ACTION = {

    Action.ADD_LEFT_TO_LEFT: "Left to left (1)",
    Action.ADD_LEFT_TO_RIGHT: "Left to right (2)",
    Action.ADD_RIGHT_TO_LEFT: "Right to left (3)",
    Action.ADD_RIGHT_TO_RIGHT: "Right to right (4)",
    Action.SPLIT: "Split (5)"
}