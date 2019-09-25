from multiprocessing import Queue, Process, Value

from control_phase.Main_thread import stop_input
from lib.frequency_spectrum.frequency_spectrum import generate_spectra
from lib.retrieve_data.retrieve_data_socket import push_random_data

def start_training():

    stop_input = Value('i')
    stop_input.value = 0
    # stored_data_batches = Array('d', 20)
    stored_data_batches = Queue()
    stored_spectrum_batches = Queue()
    # retrieve_data_process = Process(target=raw_data.store_data, args=(stored_data_batches, stop_input))
    retrieve_data_process = Process(target=push_random_data, args=(stored_data_batches, stop_input))
    analyze_data_process = Process(target=generate_spectra, args=(stored_data_batches, stored_spectrum_batches,
                                                                  stop_input))
    retrieve_data_process.start()
    analyze_data_process.start()
    # while not stop_input.value:
    #     print(stored_data_batches.get())
    # prints "[42, None, 'hello']"
    retrieve_data_process.join()
    analyze_data_process.join()