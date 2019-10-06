"""
There will be 3 threads that will elaborate the data contemporarily at different levels. to create a stack of
data_batches
Threads:
    1. Reads and stores the raw data from Arduino board (sensors). It creates data_batches of size = DATA_BATCHES_SIZE
    and it puts them into a Queue object.
    2. the Analyzer will take the object from the queue (FIFO logic) and it computes the frequency spectrum for
    data_batches
    3. It analyzes the frequency spectrum as the input to feed the ML algorithm and to predict the label (to move
    the robot arm)
"""
from multiprocessing import Queue, Process, Value

from lib.frequency_spectrum.frequency_spectrum import transform_to_spectra
from lib.retrieve_data.retrieve_data_socket import RetrieveDataSocket

def control_robot_hand():
    # raw_data = DataFromSocket()
    stop_input = Value('i')
    stop_input.value = 0
    # stored_data_batches = Array('d', 20)
    stored_data_batches = Queue()
    stored_spectrum_batches = Queue()
    # retrieve_data_process = Process(target=raw_data.store_data, args=(stored_data_batches, stop_input))
    retrieve_data_process = RetrieveDataSocket(stored_data_batches, stop_input)
    analyze_data_process = Process(target=transform_to_spectra, args=(stored_data_batches, stored_spectrum_batches,
                                                                      stop_input))
    retrieve_data_process.start()
    analyze_data_process.start()
    # while not stop_input.value:
    #     print(stored_data_batches.get())
    # prints "[42, None, 'hello']"
    retrieve_data_process.join()
    analyze_data_process.join()