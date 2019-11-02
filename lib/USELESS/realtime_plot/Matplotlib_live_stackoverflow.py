import numpy as np
import time
import matplotlib
matplotlib.use('tkagg')
from matplotlib import pyplot as plt


def randomwalk(dims=(256, 256), n=20, sigma=5, alpha=0.95, seed=1):
    """ A simple random walk with memory """

    r, c = dims
    gen = np.random.RandomState(seed)
    pos = gen.rand(2, n) * ((r,), (c,))
    old_delta = gen.randn(2, n) * sigma

    while True:
        delta = (1. - alpha) * gen.randn(2, n) * sigma + alpha * old_delta
        pos += delta
        for ii in range(n):
            if not (0. <= pos[0, ii] < r):
                pos[0, ii] = abs(pos[0, ii] % r)
            if not (0. <= pos[1, ii] < c):
                pos[1, ii] = abs(pos[1, ii] % c)
        old_delta = delta
        yield pos


def run(niter=4, doblit=True):
    """
    Display the simulation using matplotlib, optionally using blit for speed
    """

    fig, ax = plt.subplots(1, 1)
    ax.set_aspect('equal')
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    # ax.hold(True)
    rw = randomwalk()
    x, y = next(rw)

    plt.show(False)
    plt.draw()

    if doblit:
        # cache the background
        background = fig.canvas.copy_from_bbox(ax.bbox)

    points = ax.plot(x, y, 'o')[0]
    time.sleep(1)
    tic = time.time()

    for ii in range(niter):

        # update the xy data
        x, y = next(rw)
        points.set_data(x, y)

        if doblit:
            # restore background
            fig.canvas.restore_region(background)

            # redraw just the points
            ax.draw_artist(points)
            plt.draw()
            time.sleep(1)

            # fill in the axes rectangle
            fig.canvas.blit(ax.bbox)

        else:
            # redraw everything
            fig.canvas.draw()
            plt.draw()
            time.sleep(1)

    plt.close(fig)
    print("Blit = %s, average FPS: %.2f" % (
        str(doblit), niter / (time.time() - tic)) )


if __name__ == '__main__':
    run(doblit=False)
    run(doblit=True)

    # from pylab import *
    # import time
    #
    # ion()
    #
    # tstart = time.time()  # for profiling
    # x = arange(0, 2 * pi, 0.01)  # x-array
    # line, = plot(x, sin(x))
    # for i in arange(1, 200):
    #     line.set_ydata(sin(x + i / 10.0))  # update the data
    #     draw()  # redraw the canvas