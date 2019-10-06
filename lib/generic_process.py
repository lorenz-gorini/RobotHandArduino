import multiprocessing as mp

class GenericProcess(mp.Process):

    def __init__(self):
        self.exit = mp.Event()
        mp.Process.__init__(self)

    def run(self):
        pass

    def shutdown(self):
        print("Shutdown initiated")
        self.exit.set()