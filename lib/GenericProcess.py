import multiprocessing as mp

class GenericProcess(mp.Process):

    def __init__(self):
        self.exit = mp.Event()
        super().__init__()

    def run(self):
        pass

    def shutdown(self):
        print("Shutdown initiated")
        self.exit.set()