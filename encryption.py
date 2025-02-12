#Copyright (c) 2024 Eli Fisher
import os
import json
from cryptography.fernet import Fernet


def generate_key(key_file="key.key"):
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as keyfile:
            keyfile.write(key)
        print(f"Key saved to {key_file}")
    else:
        print(f"Key already exists in {key_file}")


def load_key(key_file="key.key"):
    if not os.path.exists(key_file):
        raise FileNotFoundError(f"{key_file} not found. Generate the key first.")
    with open(key_file, "rb") as keyfile:
        return keyfile.read()


def encrypt_data(data, key, output_file="keylog.enc"):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(json.dumps(data).encode())
    with open(output_file, "wb") as enc_file:
        enc_file.write(encrypted_data)
    print(f"Data encrypted and saved to {output_file}")


def decrypt_data(key, input_file="keylog.enc"):
    fernet = Fernet(key)
    with open(input_file, "rb") as enc_file:
        encrypted_data = enc_file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data)