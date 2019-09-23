"""
This will generate the dataset for the ML training
For every label we will record the data and put it in a separate folder depending on its label
"""

# TODO: INSTEAD, WE JUST COLLECT THE DATA AND STORE THEM IN THE CORRECT FOLDER! \\dataset\\{label}
from enum import Enum


class Fingers(Enum):
    thumb = 0
    index = 1
    middle = 2
    ring = 3
    pinky = 4
    all = 5

class Action(Enum):
    close = 0
    open = 1

class TrainingDataset:

    def __init__(self, action: int, finger: int):
        self.action = action
        self.finger = finger
        self.label = action * finger
    def collect(self):
        print(f"Lift the {self.finger_num}")
    def categorize(self, label):
        pass

class TrainingFingers(TrainingDataset):
    def __init__(self, action_label):
        super().__init__(action_label)

class TrainingHand(TrainingDataset):
    pass

if __name__ == "__main__":
    TrainingDataset(Action.open, Fingers.index)