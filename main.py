from control_phase.Main_thread import control_robot_hand
from lib.GestureLabels import GestureLabels
from training_phase.Training_thread import start_training

if __name__ == "__main__":
    start_training()
    # GestureLabels.get_gesture_label("open","thumb")
    # control_robot_hand()
