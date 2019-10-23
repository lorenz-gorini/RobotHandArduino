from enum import Enum
import multiprocessing as mp


total_shutdown = mp.Event()
queue_final_values = None
training_dataset_dir = ".\\training_phase\\dataset\\"

class ProcessEnum(Enum):
    retrieve_data_socket = 1,
    frequency_spectrum = 2,
    visualize_spectra = 3,
    write_to_file = 4


animation_interval = 500  # 0.5 seconds between one graph visualization and another (because only 256 points are
                          # stored every second! And we are using all of those points because the
                          # tetanic contraction frequency we expect is:
                          # 1. Around 20 Hz for UM of slow-type
                          # 2. Above  50 Hz for UM of rapid-type