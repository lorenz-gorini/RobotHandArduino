import matplotlib.pyplot as plt
import numpy as np


def generate_spectra(stored_data_batches, stored_spectrum_batches, stop_input):
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x_axis = np.arange(-5,5)
    y_axis = np.sin(x_axis)
    line1, = ax.plot(x_axis, y_axis, 'r-')
    while not stop_input.value:

        data_to_analyze = stored_data_batches.get()

        data_to_analyze = np.array(data_to_analyze)
        spectrum_batch = np.fft.fft(np.sin(data_to_analyze))
        freq = np.fft.fftfreq(data_to_analyze.shape[-1])
        # plt.plot(freq, spectrum_batch.real, freq, spectrum_batch.imag)
        # plt.show()
        line1.set_xdata(freq)
        line1.set_ydata(spectrum_batch.real)
        fig.canvas.draw()
        fig.canvas.flush_events()
        # spectrum_batch = np.fft.fft(data_to_analyze)

        # To display a ro graph --> TODO: Switch to matplotlib
        # for s in spectrum_batch:
        #     for _ in range(int(s)):
        #         print('-', sep="")
        #     print()
        print(spectrum_batch)
        stored_spectrum_batches.put(spectrum_batch)

def plot_data(x_axis, y_axis):
    # You probably won't need this if you're embedding things in a tkinter plot...
    plt.ion()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    line1, = ax.plot(x_axis, y_axis, 'r-')  # Returns a tuple of line objects, thus the comma


    line1.set_ydata(y_axis)
    fig.canvas.draw()
    fig.canvas.flush_events()