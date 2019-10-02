import random
import socket

# TODO Watch https://www.youtube.com/watch?v=GqHLztqy0PU (end)
import time

import numpy as np


class DataFromSocket:
    """
    This will be one thread that will store the data to create a stack of data_batches
    Steps:
        1. Read the single data from Arduino board (sensors)
        2. Once we store 1000 data points, it creates one data_batch
        3. It creates a stack (Queue class) of data_batches
    """

    def __init__(self, host="192.168.2.55", port=23):
        self.host = host
        self.port = port
        # Create connection to the socket
        self.mySocket = socket.socket()
        self.mySocket.connect((self.host, self.port))
        self.data_batch = []
        print("Press a key")
        self.message = input(" -> ")
    def store_data(self, stored_data_batches, is_training, stop_input):
        while not stop_input.value:
            # Create batches
            while len(self.data_batch) < 1000:
                self.mySocket.send(self.message.encode())
                single_data = self.mySocket.recv(2048).decode()
                if single_data != "\r\n":
                    self.data_batch.append(single_data)
            stored_data_batches.put(self.data_batch)
            # Consider only the first batch, if this is just for training
            if is_training.value:
                stop_input.value = 1


def push_random_data(stored_data_batches, stop_input):
    while not stop_input.value:
        # this is a function
        list_to_push = np.sin(np.arange(100))
        # these are random
            # list_to_push = []
            # for _ in range(100):
            #     list_to_push.append(random.randint(0,100))
        stored_data_batches.put(list_to_push)


if __name__ == "__main__":
    raw_data = DataFromSocket()

