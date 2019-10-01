import ctypes
import multiprocessing as mp
# from multiprocessing import Queue, Process, Value

from lib.GestureLabels import action_ids, finger_ids, moving_parts, moving_part_ids, GestureLabels
from lib.frequency_spectrum.frequency_spectrum import transform_to_spectra
from lib.frequency_spectrum.visualize_spectra import visualize_spectra
from lib.frequency_spectrum.write_to_file import write_to_file
from lib.retrieve_data.retrieve_data_socket import push_random_data

def start_training():

    stop_input = mp.Value('i')
    is_training = True
    stop_input.value = 0
    # stored_data_batches = Array('d', 20)
    stored_data_batches = mp.Queue()
    stored_spectrum_batches = mp.Queue()
    visualized_spectrum_batches = mp.Queue()
    frequency_batches = mp.Queue()
    visualized_freq_batches = mp.Queue()

    train_action, train_moving_part, train_detail_part = ask_for_user_input()
    while train_action:
        # GestureLabels.get_gesture_label(train_action,train_moving_part)
        # TODO Uncomment this when connecting the socket
        # retrieve_data_process = Process(target=raw_data.store_data, args=(stored_data_batches, stop_input))
        retrieve_data_process = mp.Process(target=push_random_data, args=(stored_data_batches, stop_input,
                                                                          is_training))
        analyze_data_process = mp.Process(target=transform_to_spectra,
                                          args=(stored_data_batches, stored_spectrum_batches, train_action,
                                                train_moving_part, stop_input))
        visualize_data_process = mp.Process(target=visualize_spectra,
                                            args=(stored_spectrum_batches, visualized_spectrum_batches,
                                                  frequency_batches, visualized_freq_batches, stop_input))
        write_to_file_process = mp.Process(target=write_to_file,
                                           args=(visualized_freq_batches, visualized_spectrum_batches,
                                                  train_action, train_moving_part, stop_input))

        retrieve_data_process.start()
        analyze_data_process.start()
        visualize_data_process.start()
        write_to_file_process.start()
        # Wait for the processes to finish
        retrieve_data_process.join()
        analyze_data_process.join()
        visualize_data_process.join()
        write_to_file_process.join()
        print("Stored. It will be very useful for training!")
        train_action, train_moving_part, train_detail_part = ask_for_user_input()

def ask_for_user_input():
    print("Tell me what you want to train next")
    train_action = input(f"Positions: \n{[f'{i}. {list(moving_parts.keys())[i]},  ' for i in range(len(moving_parts.keys()))]}")
    if train_action in  {"esc","Esc","ESC"}:
        return None, None, None

    # TODO: Improve these following lines for more details about the action!
    #  I may implement a recursive function to get to the best detail for the action. Going deeper into the dictionary
    train_moved_part = train_action = input(f"Positions: \n{[f'{i}. {list(moving_parts[0].keys())[i]},  ' for i in range(len(moving_parts['hand'].keys()))]}")
    # if train_moved_part == moving_parts[train_action]:
    #     train_detail_part = input(f"Moving Finger {[f'{c}' for c in finger_ids]}")

    return train_action, train_moved_part