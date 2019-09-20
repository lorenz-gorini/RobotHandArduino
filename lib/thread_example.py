import queue
import threading
from time import sleep
import numpy as np

if __name__ == "__main__":
    def worker():
        while True:
            item = q.get()
            if item is None:
                break
            sleep(1)
            print(item) # do_work(item)
            q.task_done()


    num_worker_threads = 23

    q = queue.Queue()
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    item_list = np.arange(0,100,1)
    for item in item_list:
        q.put(item)

    # block until all tasks are done
    q.join()

    print("fake end")
    # stop workers
    for i in range(num_worker_threads):
        # This is the key (None) to stop all the loops inside the threads!
        q.put(None)
    for t in threads:
        t.join()

    print("true end")