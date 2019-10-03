
"""
Create a CSV file to be analyzed with Machine Learning with data:
Features = coefficient for a specific frequency
Lebels = hand movement

1. Array of frequency spectra
2. Label of the hand movement

Append to this CSV file
"""
import csv
import numpy as np

def write_to_file(visualized_freq_batches, visualized_spectrum_batches,
                                                  train_action, train_moving_part):

    with open('employee_file.csv', mode='w') as employee_file:
        my_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        frequencies = visualized_freq_batches.get()
        b = np.array(['train_action', 'train_moving_part'])
        first_row = np.hstack([frequencies,b])
        my_writer.writerow(first_row)
        data_to_write = visualized_spectrum_batches.get()
        while data_to_write != []:
            b = np.array([train_action, train_moving_part])
            row_to_write = np.hstack([data_to_write, b])
            my_writer.writerow(row_to_write)
            data_to_write = visualized_spectrum_batches.get()


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