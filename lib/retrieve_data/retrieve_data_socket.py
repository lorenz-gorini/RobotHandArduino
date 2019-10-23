import random
import socket

# TODO Watch https://www.youtube.com/watch?v=GqHLztqy0PU (end)
import time
import multiprocessing as mp
import numpy as np
from lib import global_values

from lib.GenericProcess import GenericProcess

TESTING_HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
TESTING_PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

HOST_URL = "192.168.2.55"
HOST_PORT = 23

class RetrieveDataSocket(GenericProcess):
    def __init__(self, stored_data_batches:mp.Queue, is_training:bool = False):

        self.stored_data_batches = stored_data_batches
        self.is_training = is_training
        GenericProcess.__init__(self)

    def run(self):
        while not self.exit.is_set():
            # self._push_random_data()
            self._get_data_from_socket()
        print("You exited from Socket Connection!")

    def _get_data_from_socket(self):

        get_from_socket = DataFromSocket(host=TESTING_HOST, port=TESTING_PORT)
        get_from_socket.store_data(self.stored_data_batches, self.is_training)
        self.shutdown()

    # def _push_random_data(self):
    #     # THIS IS JUST A TEST FUNCTION
    #     while not self.stop_input.value:
    #         # this is a function
    #         list_to_push = np.sin(np.arange(256))+random.randint(0,5)
    #         # these are random
    #             # list_to_push = []
    #             # for _ in range(100):
    #             #     list_to_push.append(random.randint(0,100))
    #         self.stored_data_batches.put(list_to_push)
    #         time.sleep(1)
    #         # Consider only the first batch, if this is just for training
    #         # if is_training:
    #         #     stop_input.value = 1
    #     self.shutdown()


class DataFromSocket:
    """
    This will be one thread that will store the data to create a stack of data_batches
    Steps:
        1. Read the single data from Arduino board (sensors)
        2. Once we store 256 data points, it creates one data_batch
        3. It creates a stack (Queue class) of data_batches
    """

    def __init__(self, host=HOST_URL, port=HOST_PORT):

        self.host = host
        self.port = port
        # Create connection to the socket
        self.mySocket = socket.socket()
        self.mySocket.connect((self.host, self.port))
        self.data_batch = []
        print("Press a key when you are ready")
        self.message = "start"  # Line to start sending message

    def store_data(self, stored_data_batches, is_training):

        while not global_values.total_shutdown.is_set():

            self.mySocket.send(self.message.encode())
            # Create single batch list
            self.data_batch = []
            # This is to gather the full number is being sent by the socket until the chars "/r/n"
            complete_sing_data = []
            while len(self.data_batch) < 256:
                single_data = self.mySocket.recv(1024).decode()
                for i in range(len(single_data)):
                    if single_data[i] == "\r" and single_data[i+1] == "\n" :
                        self.data_batch.append(float(''.join(complete_sing_data)))
                        complete_sing_data = []
                    else:
                        complete_sing_data.append(single_data[i])
            print(self.data_batch)
            stored_data_batches.put(self.data_batch)
            # Consider only the first batch, if this is just for training
            if is_training:
                self.mySocket.sendall(str("exit").encode())
                stored_data_batches.put((global_values.queue_final_values, global_values.queue_final_values))
                break
            else:
                self.mySocket.sendall(str("continue").encode())

        self.mySocket.close()

# TODO Study how to confirm for the training datum to be stored

if __name__ == "__main__":
    raw_data = DataFromSocket()

