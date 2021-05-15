from cryptography.fernet import Fernet
import os


# get the pass.key path (generate in the current package), without this it would generate on root directory
def get_key_path():
    return os.path.join(os.path.dirname(__file__), 'pass.key')


# function to generate a new key
def _generate_key():
    key = Fernet.generate_key()
    with open(get_key_path(), "wb") as key_file:
        key_file.write(key)


# get the key, if not found generates a new one
def _call_key():
    try:
        return open(get_key_path(), "rb").read()
    except FileNotFoundError:
        _generate_key()
        print("pass.key regenerated!")
        return open(get_key_path(), "rb").read()


# funtion to encrypt a string, returns the encrypted string to push to firebase
def encrypt(slogan):
    key = _call_key()
    fernet = Fernet(key)
    coded_slogan = fernet.encrypt(str(slogan).encode())
    return coded_slogan.decode()


# function to decrypt a string from firebase, returns the decrypted string
def decrypt(coded_slogan):
    coded_slogan = str(coded_slogan)
    key = _call_key()
    fernet = Fernet(key)
    decoded_slogan = fernet.decrypt(bytes(coded_slogan, "utf-8")).decode()
    return decoded_slogan

# _generate_key() to generate a new key
