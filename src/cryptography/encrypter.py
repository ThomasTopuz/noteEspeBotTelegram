from cryptography.fernet import Fernet


def _generate_key():
    key = Fernet.generate_key()
    with open("pass.key", "wb") as key_file:
        key_file.write(key)


def _call_key():
    try:
        return open("pass.key", "rb").read()
    except FileNotFoundError:
        _generate_key()
        print("pass.key regenerated!")
        return open("pass.key", "rb").read()


def encrypt(slogan):
    key = _call_key()
    fernet = Fernet(key)
    coded_slogan = fernet.encrypt(str(slogan).encode())
    return coded_slogan.decode()


def decrypt(coded_slogan):
    coded_slogan = str(coded_slogan)
    key = _call_key()
    fernet = Fernet(key)
    decoded_slogan = fernet.decrypt(bytes(coded_slogan, "utf-8")).decode()
    return decoded_slogan

# _generate_key() to generate a new key
