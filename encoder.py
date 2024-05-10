from cryptography.fernet import Fernet
import os


class Encoder:
    @staticmethod
    def __write_key() -> None:
        with open("Encryption_Key.txt", "wb") as file:
            key = Fernet.generate_key()
            file.write(key)
            
    @staticmethod
    def __read_key() -> None:
        if not os.path.exists("Encryption_Key.txt"):
            Encoder.__write_key()
        with open("Encryption_Key.txt", "rb") as file:
            return file.read()
        
    @staticmethod
    def encrypt(entry: str) -> str:
        key = Encoder.__read_key()
        f = Fernet(key)
        encrypted = f.encrypt(entry.encode())
        return encrypted.decode()
    
    @staticmethod
    def decrypt(entry: str) -> str:
        key = Encoder.__read_key()
        f = Fernet(key)
        decrypted = f.decrypt(entry.encode())
        return decrypted.decode()
