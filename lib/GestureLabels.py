from enum import Enum

finger_ids = [
    "thumb",
    "index",
    "middle",
    "ring",
    "pinky",
    "all"
]
hand_ids = [
    "right",
    "left"
]
moving_part_ids = finger_ids
action_ids = [
    "open",
    "close"
]


class Fingers(Enum):

    thumb = finger_ids[0]
    index = finger_ids[1]
    middle = finger_ids[2]
    ring = finger_ids[3]
    pinky = finger_ids[4]
    all = finger_ids[5]

    def get_all(self):
        return finger_ids


class Hands(Enum):
    right = hand_ids[0]
    left = hand_ids[1]

class Action(Enum):
    open = action_ids[0]
    close = action_ids[1]

class GestureLabels:

    @staticmethod
    def get_gesture_label(action, moving_part):
        return moving_part + action*10

