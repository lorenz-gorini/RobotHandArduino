import numpy as np
import multiprocessing as mp
from lib.GenericProcess import GenericProcess


class TransformSpectraProcess(GenericProcess):
    def __init__(self, stored_data_batches: mp.Queue, stored_spectrum_batches: mp.Queue, frequency_batches: mp.Queue):
        super().__init__()
        self.stored_data_batches = stored_data_batches
        self.stored_spectrum_batches = stored_spectrum_batches
        self.frequency_batches = frequency_batches

    def run(self):
        while not self.exit.is_set():
            self.transform_to_spectra()
        print("You exited!")

    def transform_to_spectra(self):

        while not self.stored_data_batches.empty():

            data_to_analyze = self.stored_data_batches.get()
            data_to_analyze = np.array(data_to_analyze)
            spectrum_batch = np.fft.fft(np.sin(data_to_analyze))
            freq = np.fft.fftfreq(data_to_analyze.shape[-1])

            print(spectrum_batch)
            self.frequency_batches.put(freq)
            self.stored_spectrum_batches.put(spectrum_batch)

        # The queue is empty so we shutdown the process
        self.shutdown()


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