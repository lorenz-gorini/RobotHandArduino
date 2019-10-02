import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def visualize_spectra(stored_spectrum_batches, visualized_spectrum_batches, frequency_batches,
                      visualized_freq_batches):
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    is_queue_finished = False

    def animate(i):

        data_to_visualize = stored_spectrum_batches.get()
        freq = frequency_batches.get()
        if not data_to_visualize:
            global is_queue_finished = True
        ax1.clear()
        ax1.plot(freq, data_to_visualize.real, freq, data_to_visualize.imag)
        visualized_spectrum_batches.put(data_to_visualize)
        visualized_freq_batches.put(freq)

    an1 = animation.FuncAnimation(fig, animate, interval=1./256)
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
