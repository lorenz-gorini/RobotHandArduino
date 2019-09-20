import socket

# TODO Watch https://www.youtube.com/watch?v=GqHLztqy0PU (end)

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

        self.mySocket = socket.socket()
        self.mySocket.connect((self.host, self.port))
        self.data_batch = []
        self.stored_data = []
        print("Press a key")
        message = input(" -> ")
        while True:
            while len(self.data_batch) < 1000:
                self.mySocket.send(message.encode())
                single_data = self.mySocket.recv(2048).decode()
                if single_data != "\r\n":
                    self.data_batch.append(single_data)
            self.stored_data.append(self.data_batch)

if __name__ == "__main__":
    raw_data = DataFromSocket()

