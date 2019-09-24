import matplotlib.pyplot as plt
import numpy as np


def generate_spectra(stored_data_batches, stored_spectrum_batches, stop_input):
    while not stop_input.value:

        data_to_analyze = stored_data_batches.get()
        data_to_analyze = np.array(data_to_analyze)
        spectrum_batch = np.fft.fft(np.sin(data_to_analyze))
        freq = np.fft.fftfreq(data_to_analyze.shape[-1])
        plt.plot(freq, spectrum_batch.real, freq, spectrum_batch.imag)
        plt.show()
        # spectrum_batch = np.fft.fft(data_to_analyze)

        # To display a ro graph --> TODO: Switch to matplotlib
        # for s in spectrum_batch:
        #     for _ in range(int(s)):
        #         print('-', sep="")
        #     print()
        print(spectrum_batch)
        stored_spectrum_batches.put(spectrum_batch)