import ctypes
import multiprocessing as mp
# from multiprocessing import Queue, Process, Value

from lib.GestureLabels import action_ids, moving_part_ids, GestureLabels
from lib.frequency_spectrum.frequency_spectrum import generate_spectra
from lib.retrieve_data.retrieve_data_socket import push_random_data

def start_training():

    stop_input = mp.Value('i')
    is_training = mp.Value('b')
    stop_input.value = 0
    # stored_data_batches = Array('d', 20)
    stored_data_batches = mp.Queue()
    stored_spectrum_batches = mp.Queue()
    for train_action in action_ids:
        for train_moving_part in moving_part_ids:
            # GestureLabels.get_gesture_label(train_action,train_moving_part)
            # TODO Uncomment this when connecting the socket
            # retrieve_data_process = Process(target=raw_data.store_data, args=(stored_data_batches, stop_input))
            retrieve_data_process = mp.Process(target=push_random_data, args=(stored_data_batches, stop_input))
            analyze_data_process = mp.Process(target=generate_spectra, args=(stored_data_batches,
                                                                            stored_spectrum_batches,
                                                                          stop_input))
            start_training_process = mp.Process(target=start_training, args=(stored_spectrum_batches, stop_input,
                                                                          train_action, train_moving_part))
            # TODO Insert a boolean to distinguish is_collecting ("is_labeling"/"controlling" otherwise) or not.
            #  In that case it has to stop and register data (is it really different???)
            retrieve_data_process.start()
            analyze_data_process.start()
            start_training_process.start()
            # while not stop_input.value:
            #     print(stored_data_batches.get())
            # prints "[42, None, 'hello']"
            retrieve_data_process.join()
            analyze_data_process.join()
            start_training_process.join()

