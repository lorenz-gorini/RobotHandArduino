import numpy as np
import multiprocessing as mp
from lib.GenericProcess import GenericProcess
from lib import global_values


class TransformSpectraProcess(GenericProcess):
    def __init__(self, stored_data_batches: mp.Queue, spectrum_batches: mp.Queue):
        super().__init__()
        self.raw_data_batches = stored_data_batches
        self.spectrum_batches = spectrum_batches

    def run(self):
        while not self.exit.is_set():
            self.transform_to_spectra()
        print("You exited!")

    def transform_to_spectra(self):

        while not global_values.total_shutdown.is_set():
            if self.raw_data_batches.empty():
                continue
            else:
                data_to_analyze = self.raw_data_batches.get(timeout=5)
                if data_to_analyze is None:
                    break
                else:
                    data_to_analyze = np.array(data_to_analyze)
                    spectrum_batch = np.fft.fft(np.sin(data_to_analyze))
                    freq = np.fft.fftfreq(data_to_analyze.shape[-1])

                    print(spectrum_batch)
                    self.spectrum_batches.put((freq, spectrum_batch))

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