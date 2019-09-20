"""
There will be 3 threads that will elaborate the data contemporarily at different levels. to create a stack of
data_batches
Threads:
    1. Reads and stores the raw data from Arduino board (sensors). It creates data_batches of size = DATA_BATCHES_SIZE
    and it puts them into a Queue object.
    2. the Analyzer will take the object from the queue (FIFO logic) and it computes the frequency spectrum for
    data_batches
    3. It analyzes the frequency spectrum as the input to feed the ML algorithm and to predict the label (to move
    the robot arm)
"""
