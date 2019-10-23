import multiprocessing as mp
from lib.global_values import GlobalValues.queue_final_values, ProcessEnum

# NOT USED BECAUSE ONESINGLE QUEUE IS NOT PERFORMING WELL WHEN SEARCHING FOR UNPROCESSED DATA

class SingleBatch():

    def __init__(self, data_batch):
        self.data_batch = None
        self.last_process = 0

    def get(self, process_id: ProcessEnum):
        self._increase_process(process_id)
        return self.data_batch

    def _increase_process(self, process_id):
        if self.last_process == process_id-1:
            self.last_process = process_id
        else:
            raise BrokenPipeError("One process has been skipped. Very bad!")
