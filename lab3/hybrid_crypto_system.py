import os

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

from filehandler import FileHandler


class HybridCryptoSystem:
    @classmethod
    def generate_keys(
        self,
        encrypted_symmetric_key_dir: str,
        public_key_dir: str,
        private_key_dir: str,
        key_length: int,
    ):
        symmetric_key = os.urandom(key_length // 8)

        keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_key = keys
        public_key = keys.public_key()

        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        FileHandler.save_data(
            encrypted_symmetric_key_dir, encrypted_symmetric_key, "wb"
        )
        FileHandler.save_data(private_key_dir, private_key_pem, "wb")
        FileHandler.save_data(public_key_dir, public_key_pem, "wb")
