from cryptography.fernet import Fernet
import os


class Encoder:
    def __write_key(self) -> None:
        with open("Encryption_Key.txt", "wb") as file:
            key = Fernet.generate_key()
            file.write(key)

    def __read_key(self) -> None:
        if not os.path.exists("Encryption_Key.txt"):
            self.__write_key()
        with open("Encryption_Key.txt", "rb") as file:
            self.__key = file.read()

    def __init__(self) -> None:
        self.__read_key()

    def encrypt(self, entry: str) -> str:
        f = Fernet(self.__key)
        encrypted = f.encrypt(entry.encode())
        return encrypted.decode()

    def decrypt(self, entry: str) -> str:
        f = Fernet(self.__key)
        decrypted = f.decrypt(entry.encode())
        return decrypted.decode()
