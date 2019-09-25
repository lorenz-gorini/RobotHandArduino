from enum import Enum

finger_ids = {
    "thumb": 0,
    "index": 1,
    "middle": 2,
    "ring": 3,
    "pinky": 4,
    "all": 5
}
action_ids = {
    "open": 0,
    "close": 1
}
hand_ids = {
    "right": 0,
    "left": 1
}

class Fingers(Enum):
    thumb = finger_ids["thumb"]
    index = finger_ids["index"]
    middle = finger_ids["middle"]
    ring = finger_ids["ring"]
    pinky = finger_ids["pinky"]
    all = finger_ids["all"]

class Hands(Enum):
    right = hand_ids["right"]
    left = hand_ids["left"]

class Action(Enum):
    close = action_ids["open"]
    open = action_ids["close"]

class GestureLabels:

    @staticmethod
    def get_gesture_label(action, moving_part):
        return moving_part + action*10

