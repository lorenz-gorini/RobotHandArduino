import queue

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np
import multiprocessing as mp


# def visualize_spectra_TEST(stored_spectrum_batches, frequency_batches):
#     fig = plt.figure()
#     ax1 = fig.add_subplot(1, 1, 1)
#     is_queue_finished = False
#
#     ax = plt.axis([0,256,0,256])
#     iter_x = iter(frequency_batches)
#     iter_y = iter(stored_spectrum_batches)
#     data_to_visualize = next(iter_y)
#     freq = next(iter_x)
#     freq_signal, = ax1.plot(freq, data_to_visualize.real)
#
#     def animate(i):
#         try:
#             data_to_visualize = next(iter_y)
#             freq = next(iter_x)
#             freq_signal.set_data(freq, data_to_visualize.real)
#             return freq_signal,
#         except StopIteration:
#             an1.event_source.stop()
#             return freq_signal,
#
#
#     an1 = animation.FuncAnimation(fig, animate, interval=300, blit=True)
#     plt.show()
from lib.GenericProcess import GenericProcess


class VisualizeSpectraProcess(GenericProcess):
    def __init__(self, stored_spectrum_batches: mp.Queue, visualized_spectrum_batches: mp.Queue,
                                                      frequency_batches: mp.Queue, visualized_freq_batches: mp.Queue):
        super().__init__()
        self.stored_spectrum_batches = stored_spectrum_batches
        self.visualized_spectrum_batches = visualized_spectrum_batches
        self.frequency_batches = frequency_batches
        self.visualized_freq_batches = visualized_freq_batches

    def run(self):
        while not self.exit.is_set():
            self._visualize_spectra()
        print("You exited!")


    def _visualize_spectra(self):

        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)

        ax = plt.axis([-1,1, -50, 50])

        AnimatedGraph(fig, ax1, self.stored_spectrum_batches,
                      self.visualized_spectrum_batches,
                      self.frequency_batches, self.visualized_freq_batches)
        self.shutdown()


class AnimatedGraph():
    def __init__(self, fig, ax1, stored_spectrum_batches: mp.Queue, visualized_spectrum_batches: mp.Queue,
                                                      frequency_batches: mp.Queue, visualized_freq_batches: mp.Queue):
        self.stored_spectrum_batches = stored_spectrum_batches
        self.visualized_spectrum_batches = visualized_spectrum_batches
        self.frequency_batches = frequency_batches
        self.visualized_freq_batches = visualized_freq_batches

        self.freq_signal_real, self.freq_signal_imag = ax1.plot([0],[0],[0],[0])
        self.anim_graph = animation.FuncAnimation(fig, self.animate, interval=1)
        plt.show()

        plt.close()

    def animate(self,i):
        try:
            data_to_visualize = self.stored_spectrum_batches.get(timeout=5)
            freq = self.frequency_batches.get(timeout=1)
            self.freq_signal_real.set_data(freq, data_to_visualize.real)
            self.freq_signal_imag.set_data(freq, data_to_visualize.imag)
            self.visualized_spectrum_batches.put(data_to_visualize)
            self.visualized_freq_batches.put(freq)
            return self.freq_signal_real, self.freq_signal_imag
        except queue.Empty:
            time.sleep(2)
            self.anim_graph.event_source.stop()
            # TODO How to make it work also during training mode with only one batch and to keep it still for few
            #  seconds once the queue is empty???
            plt.close()
            return

# TODO All the function
def visualize_raw_signal(stored_spectrum_batches, visualized_spectrum_batches, frequency_batches,
                      visualized_freq_batches, stop_input):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    def animate(i):

        data_to_visualize = stored_spectrum_batches.get()
        freq = frequency_batches.get()

        ax1.clear()
        ax1.plot(freq, data_to_visualize.real, freq, data_to_visualize.imag)
        visualized_spectrum_batches.put(data_to_visualize)
        visualized_freq_batches.put(freq)

    an1 = animation.FuncAnimation(fig, animate, interval=1./256)
    plt.show()
    while not stop_input:
        time.sleep(0.05)
    plt.close()

if __name__ == "__main__":
    stored_spectrum_batches = []
    frequency_batches = []
    for i in range(10):
        stop_value = 256.*((i+1)/10.)
        stored_spectrum_batches.append(np.arange(0, stop_value, (i+1)/10.))
        frequency_batches.append(np.arange(0, 256, 1))
    # visualize_spectra_TEST(stored_spectrum_batches, frequency_batches)
