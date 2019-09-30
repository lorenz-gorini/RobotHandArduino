import ctypes
import multiprocessing as mp
# from multiprocessing import Queue, Process, Value

from lib.GestureLabels import action_ids, finger_ids, moving_parts, moving_part_ids, GestureLabels
from lib.frequency_spectrum.frequency_spectrum import transform_to_spectra
from lib.frequency_spectrum.visualize_spectra import visualize_spectra
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
        # GestureLabels.get_gesture_label(train_action,train_moving_part)
        # TODO Uncomment this when connecting the socket
        # retrieve_data_process = Process(target=raw_data.store_data, args=(stored_data_batches, stop_input))
        retrieve_data_process = mp.Process(target=push_random_data, args=(stored_data_batches, stop_input,
                                                                          is_training))
        analyze_data_process = mp.Process(target=transform_to_spectra, args=(stored_data_batches,
                                                                             stored_spectrum_batches,
                                                                             train_action, train_moving_part,
                                                                             stop_input))
        visualize_data_process = mp.Process(target=visualize_spectra,
                                            args=(stored_spectrum_batches, visualized_spectrum_batches,
                                                  frequency_batches, visualized_freq_batches,
                                                  train_action, train_moving_part, stop_input))
        # TODO Insert a boolean to distinguish is_collecting ("is_labeling"/"controlling" otherwise) or not.
        #  In that case it has to stop and register data (is it really different???)
        retrieve_data_process.start()
        analyze_data_process.start()
        visualize_data_process.start()
        # while not stop_input.value:
        #     print(stored_data_batches.get())
        # prints "[42, None, 'hello']"
        retrieve_data_process.join()
        analyze_data_process.join()
        visualize_data_process.join()

def ask_for_user_input():
    print("Tell me what you want to train next")
    train_action = input(f"Position {[f'{c}' for c in action_ids]}")
    if train_action in  {"esc","Esc","ESC"}:
        return None, None, None

    train_moving_part = input(f"Moving Part {[f'{c}' for c in moving_parts]}")
    # TODO:
    if train_moving_part == 1:
        train_detail_part = input(f"Moving Finger {[f'{c}' for c in finger_ids]}")

    return train_moving_part