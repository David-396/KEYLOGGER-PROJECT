import json
import base64
from cryptography.fernet import Fernet

#import the encrypted data
from encryption import encrypted_dic

#the encrypted data
encrypted=encrypted_dic

#create a key base on the mac address
def get_key(mac_address):
    final_mac_add = mac_address.replace(":","f") #get mac address and replace ":" white "f"
    base_key = f"fp88{final_mac_add}wAxDAAjijM=" #our key for the decryption
    final_key=base64.urlsafe_b64encode(base_key.encode()) #convert to base64
    return final_key

def decrypt_data(encrypted_data,key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())

# Example
key=get_key("f8:54:f6:bc:2e:64")
decrypt=decrypt_data(encrypted,key)

if __name__ == "__main__":
    print("🔑 key:",key)
    print("🔒 decrypted data:",decrypt)

