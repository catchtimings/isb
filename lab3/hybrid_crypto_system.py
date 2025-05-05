import os

from cryptography.hazmat.primitives import hashes, serialization, padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES

from filehandler import FileHandler


class HybridCryptoSystem:
    def __init__(self, length=128):
        self.__key_length = length

    def generate_keys(
        self,
        encrypted_symmetric_key_dir: str,
        public_key_dir: str,
        private_key_dir: str,
    ):
        symmetric_key = os.urandom(self.__key_length // 8)

        keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_key = keys
        public_key = keys.public_key()

        encrypted_symmetric_key = self.__encrypt_symmetric_key(
            public_key, symmetric_key
        )

        FileHandler.save_data(
            encrypted_symmetric_key_dir, encrypted_symmetric_key, "wb"
        )
        self.__serialization_rsa_key(private_key_dir, private_key, "private")
        self.__serialization_rsa_key(public_key_dir, public_key, "public")

    def encrypt_data(
        self,
        plain_text_dir: str,
        private_key_dir: str,
        encrypted_symmetric_key_dir: str,
        encrypted_data_dir: str,
    ):
        if not (plain_text := FileHandler.read_data(plain_text_dir, "rb")):
            raise ValueError("Text file must not be empty")
        if not (private_bytes := FileHandler.read_data(private_key_dir, "rb")):
            raise ValueError("Private key must not be empty")
        if not (encrypted_symmetric_key := FileHandler.read_data(encrypted_symmetric_key_dir, "rb")):
            raise ValueError("Encrypted symmetric key must not be empty")

        private_key = self.__deserialization_rsa_key(private_bytes, "private")
        symmetric_key = self.__decrypt_symmetric_key(encrypted_symmetric_key, private_key)

        padder = padding.ANSIX923(self.__key_length).padder()
        padded_text = padder.update(plain_text) + padder.finalize()

        iv = os.urandom(8)
        cipher = Cipher(TripleDES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_text = encryptor.update(padded_text) + encryptor.finalize()

        FileHandler.save_data(encrypted_data_dir, encrypted_text, "wb")

    def __serialization_rsa_key(self, key_dir, key, key_type):
        match key_type:
            case "private":
                private_key_pem = key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
                FileHandler.save_data(key_dir, private_key_pem, "wb")
            case "public":
                public_key_pem = key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
                FileHandler.save_data(key_dir, public_key_pem, "wb")

    def __deserialization_rsa_key(self, key, key_type):
        match key_type:
            case "private":
                return serialization.load_pem_private_key(key, password=None)
            case "public":
                return serialization.load_pem_public_key(key)

    def __encrypt_symmetric_key(self, public_key, symmetric_key):
        return public_key.encrypt(
            symmetric_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

    def __decrypt_symmetric_key(self, encrypted_symmetric_key, private_key):
        return private_key.decrypt(
            encrypted_symmetric_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )