from cryptography.fernet import Fernet
from getmac import get_mac_address
import json

class Encrypt:
    def __init__(self):
        self._key = Fernet.generate_key()

    def encrypt_data(self, data, output_file="keylog.enc"):
        fernet = Fernet(self._key)
        encrypted_data = fernet.encrypt(json.dumps(data).encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        fernet = Fernet(self._key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data)

# print(len(Encrypt()._key))
# print(Encrypt().encrypt_data({1:2,3:4}))
# print(len(Encrypt()._key))
# e=Encrypt().encrypt_data({1:2,3:4})
# print(bytes(e))
# print(Encrypt().decrypt_data(bytes(e)))

print({1:{2:{3:9}}})