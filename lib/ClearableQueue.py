
from multiprocessing.queues import Queue

class ClearableQueue(Queue):

    def __init__(self):
        super().__init__()

    def clear(self):
        while not self.empty():
            self.get()  # as docs say: Remove and return an item from the queue.