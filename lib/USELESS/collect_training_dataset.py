"""
This will generate the dataset for the ML training
For every label we will record the data and put it in a separate folder depending on its label
(watch code from: https://youtu.be/qbW6FRbaSl0?t=199 )
"""
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import json
import time


DATA_COLLECTING_FOLDER = ".\\data_collecting_folder\\" # os.path.join(LIB_FOLDER,".\\")

class MyHandler(FileSystemEventHandler):
    i=1
    def on_modified(self, event):
        new_name = f"spectrum_{time.time_ns()}"
        folder_destination = os.path.join(DATA_COLLECTING_FOLDER,f"{label}\\")
        for filename in os.listdir(DATA_COLLECTING_FOLDER):
            # Rename the file to a timestamp (we care only about the label that will be in the folder name)
            source_file = DATA_COLLECTING_FOLDER + "\\" + filename
            os.rename(source_file, folder_destination+"\\"+new_name)

# To complete, see youtube video above