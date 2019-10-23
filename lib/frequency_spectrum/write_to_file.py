
"""
Create a CSV file to be analyzed with Machine Learning with data:
Features = coefficient for a specific frequency
Lebels = hand movement

1. Array of frequency spectra
2. Label of the hand movement

Append to this CSV file
"""
import csv
import os

import numpy as np
from lib import global_values
from lib.GenericProcess import GenericProcess
import multiprocessing as mp




class WriteFileProcess(GenericProcess):

    def __init__(self, visualized_batches: mp.Queue, train_action: mp.Value, train_moving_part: mp.Value):
        super().__init__()
        self.visualized_batches = visualized_batches
        self.train_action = train_action
        self.train_moving_part = train_moving_part
        self.employee_file = open(os.path.join(global_values.training_dataset_dir, 'collected_dataset.txt'), mode='w')
        self.my_writer = csv.writer(self.employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        self.is_first_row = True

    def run(self):
        while not self.exit.is_set():
            self._write_to_file()
        print("You exited!")

    def _write_to_file(self):

        while not global_values.total_shutdown.is_set():
            if self.visualized_batches.empty():
                continue
            else:
                freq_batch, data_to_write = self.visualized_batches.get(timeout=5)
                if len(freq_batch) == 1 and len(data_to_write) == 1:
                    break
                else:
                    if self.is_first_row:
                        labels = np.array(['train_action', 'train_moving_part'])
                        first_row = np.hstack([data_to_write, labels])
                        self.my_writer.writerow(first_row)
                        self.is_first_row = False

                    labels = np.array([self.train_action.value, self.train_moving_part.value])
                    row_to_write = np.hstack([data_to_write, labels])
                    self.my_writer.writerow(row_to_write)
        self.shutdown()

    # data_to_analyze = stored_data_batches.get()
    # while data_to_analyze:
    #     data_to_analyze = np.array(data_to_analyze)
    #     spectrum_batch = np.fft.fft(np.sin(data_to_analyze))
    #     freq = np.fft.fftfreq(data_to_analyze.shape[-1])
    #
    #     print(spectrum_batch)
    #     frequency_batches.put(freq)
    #     stored_spectrum_batches.put(spectrum_batch)
    #
    #     data_to_analyze = stored_data_batches.get()