import numpy as np


def generate_spectra(stored_data_batches, stored_spectrum_batches, stop_input):
    while not stop_input.value:
        data_to_analyze = stored_data_batches.get()
        spectrum_batch = np.fft.fft(data_to_analyze)
        # To display a ro graph --> TODO: Switch with matplotlib
        # for s in spectrum_batch:
        #     for _ in range(int(s)):
        #         print('-', sep="")
        #     print()
        print(spectrum_batch)
        stored_spectrum_batches.put(spectrum_batch)