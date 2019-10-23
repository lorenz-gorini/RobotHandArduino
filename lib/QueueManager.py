
import multiprocessing as mp


from lib.SingleBatch import SingleBatch
from lib.global_values import GlobalValues, ProcessEnum
from training_phase.Training_thread import total_shutdown

# THIS IS NOT USED BECAUSE IT IS MUCH BETTER TO HAVE SEPARATE QUEUES

class QueueManager():

    def __init__(self):
        self.stored_data_batches = mp.Queue()
        self.stored_spectrum_batches = mp.Queue()
        self.visualized_spectrum_batches = mp.Queue()
        self.queue_dict = {
            ProcessEnum.retrieve_data_socket: self.stored_data_batches,
            ProcessEnum.frequency_spectrum: self.stored_spectrum_batches,
            ProcessEnum.visualize_spectra: self.visualized_spectrum_batches
        }

    def get_by_id(self, process_id: ProcessEnum):
        while not total_shutdown.is_set():
            if self.queue_dict[process_id].empty():
                continue
            else:
                next_value = self.queue_dict[process_id].get(block=True, timeout=0.05)

            return next_value
        return GlobalValues.queue_final_values

    #TODO
    def remove(self):
        if not self.data_pipe.empty():
            return self.data_pipe.get(timeout=5)
        else:
            raise BrokenPipeError("The Queue is empty but it has not been closed. Some process got stuck")

    def close(self, process_id, processes_num=1):
        for p in range(processes_num):
            self.queue_dict[process_id].put(GlobalValues.queue_final_values)

    #TODO
    def add(self, batch: SingleBatch, process_id: ProcessEnum):
        if process_id == ProcessEnum.retrieve_data_socket:
            sing_batch = SingleBatch(batch)
            self.data_pipe.put(sing_batch)
        else:
            raise PermissionError(f"The process {process_id} is not allowed to "
                                  f"introduce a new batch inside the queue")

