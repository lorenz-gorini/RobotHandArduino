import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np


def visualize_spectra_TEST(stored_spectrum_batches, frequency_batches):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    is_queue_finished = False

    ax = plt.axis([0,256,0,256])
    iter_x = iter(frequency_batches)
    iter_y = iter(stored_spectrum_batches)
    data_to_visualize = next(iter_y)
    freq = next(iter_x)
    freq_signal, = ax1.plot(freq, data_to_visualize.real) # , freq, data_to_visualize.imag)

    def animate(i):
        try:
            data_to_visualize = next(iter_y)
            freq = next(iter_x)
            freq_signal.set_data(freq, data_to_visualize.real)  # , freq, data_to_visualize.imag
            return freq_signal,
        except StopIteration:
            an1.event_source.stop()
            return freq_signal,


    an1 = animation.FuncAnimation(fig, animate, interval=10, blit=True)
    plt.show()


def visualize_spectra(stored_spectrum_batches, visualized_spectrum_batches,
                                                  frequency_batches, visualized_freq_batches):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    is_queue_finished = False

    ax = plt.axis([0, 1000, 0, 256])
    data_to_visualize = stored_spectrum_batches.get()
    freq = frequency_batches.get()
    freq_signal_real, freq_signal_imag = ax1.plot(freq, data_to_visualize.real, freq, data_to_visualize.imag)

    def animate(i):

        data_to_visualize = stored_spectrum_batches.get()
        freq = frequency_batches.get()
        if data_to_visualize == []:
            global is_queue_finished
            is_queue_finished = True
        freq_signal_real.set_data(freq, data_to_visualize.real)
        freq_signal_imag.set_data(freq, data_to_visualize.imag)
        visualized_spectrum_batches.put(data_to_visualize)
        visualized_freq_batches.put(freq)

    an1 = animation.FuncAnimation(fig, animate, interval=15)
    plt.show()
    while not is_queue_finished:
        time.sleep(0.05)
    plt.close()

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
    visualize_spectra_TEST(stored_spectrum_batches, frequency_batches)
