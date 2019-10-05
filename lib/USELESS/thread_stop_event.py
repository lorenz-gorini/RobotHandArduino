from queue import Queue
from threading import Thread
import sys

_sentinel = object()

class Worker(Thread):
    def __init__(self, queue, sentinel=None):
        # Call thread constructor
        self.queue = queue
        self.sentinel = sentinel
        super(Worker, self).__init__()

    def run(self):
        while True:
            task = self.queue.get()
            print(task)
            if task is self.sentinel:
                self.queue.task_done()
                return
            # doTask()
            self.queue.task_done()


# queue = Queue()
# thread = Worker(queue, sentinel=_sentinel)
# thread.start()
#
# while True:
#     inp = input()
#
#     if inp:
#         queue.put(inp)
#     else:
#         queue.put(_sentinel)
#         queue.join()
#         thread.join()
#         sys.exit(0)

class Anim():
    def __init__(self, fig, **kw):
        self.reward=0
        self.ani = animation.FuncAnimation(fig, self.animate,
                                           frames=100, repeat = False)

    def animate(self,i):
        reward = update(reward)
        some_object[i] = func(reward)
        if self.reward > 10:
            self.ani.event_source.stop()
        return some_object


import multiprocessing
import time

class MyProcess(multiprocessing.Process):

    def __init__(self, ):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()

    def run(self):
        while not self.exit.is_set():
            pass
        print("You exited!")

    def shutdown(self):
        print("Shutdown initiated")
        self.exit.set()


if __name__ == "__main__":
    process = MyProcess()
    process.start()
    print("Waiting for a while")
    time.sleep(3)
    process.shutdown()
    time.sleep(3)
    print("Child process state: %d" % process.is_alive())
    process.join()
    print("Done")