# from control_phase.Main_thread import control_robot_hand
from training_phase.Training_thread import start_training

if __name__ == "__main__":
    start_training()
    # control_robot_hand()  # This is needed to control after the training
