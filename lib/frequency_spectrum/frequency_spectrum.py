import matplotlib.pyplot as plt
import numpy as np


def transform_to_spectra(stored_data_batches, stored_spectrum_batches, frequency_batches):

    data_to_analyze = stored_data_batches.get()
    while data_to_analyze != []:

        data_to_analyze = np.array(data_to_analyze)
        spectrum_batch = np.fft.fft(np.sin(data_to_analyze))
        freq = np.fft.fftfreq(data_to_analyze.shape[-1])

        print(spectrum_batch)
        frequency_batches.put(freq)
        stored_spectrum_batches.put(spectrum_batch)

        data_to_analyze = stored_data_batches.get()


#
# def plot_data(x_axis, y_axis):
#     # You probably won't need this if you're embedding things in a tkinter plot...
#     plt.ion()
#
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     line1, = ax.plot(x_axis, y_axis, 'r-')  # Returns a tuple of line objects, thus the comma
#
#
#     line1.set_ydata(y_axis)
#     fig.canvas.draw()
#     fig.canvas.flush_events()