from enum import Enum
import hashlib

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
# moving_parts.keys will always return lists of the possible things to do...
# even though this may not be the perfect implementation
moving_parts = {
    "hand": { "open": 0, "close": 1},
    "wrist": { "move_left":0, "move_right":1, "move_up":2, "move_down": 3},
    "arm": 2,
    "finger": { "open": {"thumb": 0, "index": 1, ".....": 2}, "close": {"thumb": 0, "index": 1, ".....": 2}},
}
moving_part_ids = finger_ids.extend(hand_ids)
action_ids = {
    "open": 0,
    "close": 1
}

# I may even think that the user is able to add new actions! but it could be a mess
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

class BodyParts(Enum):
    hand = "hand"
    wrist = "wrist"
    arm = "arm"

class Action(Enum):
    open = action_ids[0]
    close = action_ids[1]

class GestureLabels:

    @staticmethod
    def get_gesture_label(action:str, moving_part:str):
        # Hashing is too slow. It is better to use a dictionary with indexes.
        # Integrated hash function is not consistent throughout the processes and we need
        # something that will be replicated always (label stays the same).
        # Infact a dictionary is exactly hashing!!!
        # return moving_part + action*100

        hash_object = hashlib.sha256((moving_part + action*100).encode('UTF-8'))
        hex_dig = hash_object.hexdigest()
        return (hex_dig)
