import os

from cryptography.hazmat.primitives import hashes, serialization, padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES

from filehandler import FileHandler


class HybridCryptoSystem:
    """Hybrid CryptoSystem class"""

    def __init__(self, length=128):
        """
        Initializing the system
        :param length: key length, default value=128 bits
        """
        self.__key_length = length

    def generate_keys(
        self,
        encrypted_symmetric_key_dir: str,
        public_key_dir: str,
        private_key_dir: str,
    ):
        """
        Key generation method
        :param encrypted_symmetric_key_dir: directory to save encrypted symmetric key
        :param public_key_dir: directory to save public asymmetric key
        :param private_key_dir: directory to save private asymmetric key
        :return None
        """
        symmetric_key = os.urandom(self.__key_length // 8)

        keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_key = keys
        public_key = keys.public_key()

        s_private_key = self.__serialization_rsa_key(private_key, "private")
        s_public_key = self.__serialization_rsa_key(public_key, "public")

        encrypted_symmetric_key = self.__encrypt_symmetric_key(
            symmetric_key, public_key
        )

        FileHandler.save_data(
            encrypted_symmetric_key_dir, encrypted_symmetric_key, "wb"
        )
        FileHandler.save_data(private_key_dir, s_private_key, "wb")
        FileHandler.save_data(public_key_dir, s_public_key, "wb")

    def encrypt_data(
        self,
        plain_text_dir: str,
        private_key_dir: str,
        encrypted_symmetric_key_dir: str,
        encrypted_data_dir: str,
    ):
        """
        Data encryption method
        :param plain_text_dir: directory to file with text to encrypt
        :param private_key_dir: directory to private asymmetric key
        :param encrypted_symmetric_key_dir: directory to symmetric key
        :param encrypted_data_dir: directory to save encrypted data
        :return:
        """
        if not (plain_text := FileHandler.read_data(plain_text_dir, "rb")):
            raise ValueError("Text file must not be empty")
        if not (private_bytes := FileHandler.read_data(private_key_dir, "rb")):
            raise ValueError("Private key must not be empty")
        if not (encrypted_symmetric_key := FileHandler.read_data(encrypted_symmetric_key_dir, "rb")):
            raise ValueError("Encrypted symmetric key must not be empty")

        private_key = self.__deserialization_rsa_key(private_bytes, "private")
        symmetric_key = self.__decrypt_symmetric_key(
            encrypted_symmetric_key, private_key
        )

        padder = padding.ANSIX923(64).padder()
        padded_text = padder.update(plain_text) + padder.finalize()

        iv = os.urandom(8)
        cipher = Cipher(TripleDES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_text = encryptor.update(padded_text) + encryptor.finalize()

        FileHandler.save_data(encrypted_data_dir, encrypted_text + iv, "wb")

    def decrypt_data(
        self,
        encrypted_text_dir: str,
        private_key_dir: str,
        encrypted_symmetric_key_dir: str,
        decrypted_text_dir: str,
    ):
        """
        Decryption data method
        :param encrypted_text_dir: directory to file with text to decrypt
        :param private_key_dir: directory to private asymmetric key
        :param encrypted_symmetric_key_dir: directory to symmetric key
        :param decrypted_text_dir: irectory to save decrypted data
        :return: None
        """
        if not (encrypted_text := FileHandler.read_data(encrypted_text_dir, "rb")):
            raise ValueError("Text file must not be empty")
        if not (private_bytes := FileHandler.read_data(private_key_dir, "rb")):
            raise ValueError("Private key must not be empty")
        if not (encrypted_symmetric_key := FileHandler.read_data(encrypted_symmetric_key_dir, "rb")):
            raise ValueError("Encrypted symmetric key must not be empty")

        private_key = self.__deserialization_rsa_key(private_bytes, "private")
        symmetric_key = self.__decrypt_symmetric_key(
            encrypted_symmetric_key, private_key
        )

        iv = encrypted_text[-8:]
        text = encrypted_text[:-8]
        cipher = Cipher(TripleDES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_text = decryptor.update(text) + decryptor.finalize()

        unpadder = padding.ANSIX923(64).unpadder()
        decrypted_text = unpadder.update(padded_text) + unpadder.finalize()

        FileHandler.save_data(decrypted_text_dir, decrypted_text, "wb")

    def __serialization_rsa_key(self, key, key_type):
        """
        Serialization rsa asymmetric key
        :param key_dir: directory to save the key
        :param key: key to save
        :param key_type: type of key - private or public
        :return: serialized key
        """
        match key_type:
            case "private":
                return key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            case "public":
                return key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )

    def __deserialization_rsa_key(self, key, key_type):
        """
        Deserialization rsa asymmetric key
        :param key: the key to deserialize
        :param key_type: type of key - private or public
        :return: None
        """
        match key_type:
            case "private":
                return serialization.load_pem_private_key(key, password=None)
            case "public":
                return serialization.load_pem_public_key(key)

    def __encrypt_symmetric_key(self, symmetric_key, public_key):
        """
        Symmetric key encryption method
        :param symmetric_key: the key to encrypt
        :param public_key: public asymmetric key
        :return: encrypted symmetric key
        """
        return public_key.encrypt(
            symmetric_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

    def __decrypt_symmetric_key(self, encrypted_symmetric_key, private_key):
        """
        Symmetric key decryption method
        :param encrypted_symmetric_key: the key to decrypt
        :param private_key: private asymmetric key
        :return: decrypted symmetric key
        """
        return private_key.decrypt(
            encrypted_symmetric_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
