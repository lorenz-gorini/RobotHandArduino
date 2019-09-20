"""
This will generate the dataset for the ML training
For every label we will record the data and put it in a separate folder depending on its label
(watch code from: https://youtu.be/qbW6FRbaSl0?t=199 )
"""
from watchdog.observers import read_directory_changes
from watchdog.events import FileSystemEventHandler

import os
import json
import time


DATA_COLLECTING_FOLDER = ".\\" # os.path.join(LIB_FOLDER,".\\")

class MyHandler(FileSystemEventHandler):
    i=1
    def on_modified(self, event):
        new_name = "test"
        for filename in os.listdir(DATA_COLLECTING_FOLDER):
            # Rename the file
