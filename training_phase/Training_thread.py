import ctypes
import multiprocessing as mp

from lib.GestureLabels import action_ids, finger_ids, moving_parts, moving_part_ids, GestureLabels
from lib.frequency_spectrum.frequency_spectrum import TransformSpectraProcess
from lib.frequency_spectrum.visualize_spectra import VisualizeSpectraProcess, visualize_realtime_TEST
from lib.frequency_spectrum.write_to_file import WriteFileProcess
from lib.retrieve_data.retrieve_data_socket import RetrieveDataSocket

class ProcessManager:
    #TODO Implement this to manage the processes
    def __init__(self):
        self.processes = []

    def start_processes(self):
        for p in self.processes:
            p.start()

    def join_processes(self):
        for p in self.processes:
            p.join()



def start_training():

    train_moving_part = mp.Value('i')
    train_action = mp.Value('i')

    is_training = False  # TODO true

    action_input, moving_part_input = ask_for_user_input()  # TODO , train_detail_part
    train_action.value = action_input
    train_moving_part.value = moving_part_input
    while train_action.value is not None:
        confirm_data_input = ''
        while confirm_data_input.lower() != 'y':
            # Clear queues and values
            raw_data_batches = mp.Queue()
            spectrum_batches = mp.Queue()
            visualized_batches = mp.Queue()

            retrieve_data_process = RetrieveDataSocket(raw_data_batches, is_training)
            spectra_process = TransformSpectraProcess(raw_data_batches, spectrum_batches)
            visualize_data_process = mp.Process(target=visualize_realtime_TEST, args=(spectrum_batches, visualized_batches))


            # VisualizeSpectraProcess(spectrum_batches, visualized_batches)
            write_to_file_process = WriteFileProcess(visualized_batches, train_action, train_moving_part)

            retrieve_data_process.start()
            spectra_process.start()
            visualize_data_process.start()
            # write_to_file_process.start()
            # Wait for the processes to finish
            # The processes will stop when the elements of the queues generated by
            # retrieve_data_process will all be analyzed.
            # And the function retrieve_data_process will stop depending on what we set:
            # 1. We choose the highest values in an interval of 2-3 seconds
            # 2. We analyze only the first batch
            # 3. ...

            # In the controller_mode, instead, we will stop when we input something on the keyboard for example,
            # or the connection with the socket is lost
            retrieve_data_process.join()
            spectra_process.join()
            visualize_data_process.join()
            # write_to_file_process.join()
            confirm_data_input = input("Is the graph what you were looking for?(y/n)")
        print("Stored. It will be very useful for training!")
        train_action, train_moving_part = ask_for_user_input()  # , train_detail_part
        train_action.value = action_input
        train_moving_part.value = moving_part_input
    print("Exiting. See you soon!")

def ask_for_user_input():
    print("Tell me what you want to train next")
    action_input = input(f"""Positions: \n{
                        [f'{i}. {list(moving_parts.keys())[i]},  ' for i in range(len(moving_parts.keys()))]}"""
                         f"\n Esc : finish training")
    if action_input.lower() == "esc":
        return None, None

    # TODO: Improve these following lines for more details about the action!
    #  I may implement a recursive function to get to the best detail for the action. Going deeper into the dictionary
    moving_part_input = action_input = input(f"""Positions: \n{
                                            [f"{i}. {list(moving_parts['hand'].keys())[i]},  "
                                             for i in range(len(moving_parts['hand'].keys()))]}""")
    # if train_moved_part == moving_parts[train_action]:
    #     train_detail_part = input(f"Moving Finger {[f'{c}' for c in finger_ids]}")

    return int(action_input), int(moving_part_input)