from cryptography.fernet import *


def genwrite_key():
    key = Fernet.generate_key()
    with open("pass.key", "wb") as key_file:
        key_file.write(key)

# genwrite_key()


def call_key():
    return open("pass.key", "rb").read()


def encrypt(nota):
    slogan = bytes(str(nota), 'utf-8')
    key = call_key()
    a = Fernet(key)
    coded_slogan = a.encrypt(slogan)
    return coded_slogan


def decrypt(coded_slogan):
    key = call_key()
    b = Fernet(key)
    decoded_slogan = b.decrypt(coded_slogan)
    return decoded_slogan

