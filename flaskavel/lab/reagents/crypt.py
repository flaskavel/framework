import os
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class Crypt:
    """
    Provides static methods to encrypt and decrypt values using AES-GCM encryption.
    """

    @staticmethod
    def encrypt(value: str) -> str:
        """
        Encrypts a given plaintext using AES-GCM encryption.

        :param value: The plaintext value to be encrypted.
        :return: Encrypted string in the format "ciphertextΔivΔtag".
        """
        return _Encryption().encrypt(plaintext=value)

    @staticmethod
    def decrypt(value: str) -> str:
        """
        Decrypts a given encrypted string using AES-GCM decryption.

        :param value: The encrypted string to be decrypted.
        :return: Decrypted plaintext string.
        """
        return _Encryption().decrypt(encrypted_data=value)


class _Encryption:
    """
    Handles encryption and decryption using AES-GCM with dynamic key size (128, 192, or 256 bits).
    """

    def __init__(self, key: str = None, key_size: int = 256):
        """
        Initializes the encryption class with a given key or generates one if not provided.

        :param key: Optional encryption key (string). If not provided, a key is derived from the file path.
        :param key_size: Size of the key to be used (128, 192, or 256 bits). Defaults to 256 bits.
        :raises ValueError: If key_size is not 128, 192, or 256.
        """
        if key_size not in [128, 192, 256]:
            raise ValueError("Key size must be 128, 192, or 256 bits.")

        self.key_size = key_size
        self.separator = hashlib.sha256(str(os.path.abspath(__file__)).encode()).hexdigest()
        self.key = self._derive_key(key, key_size)

    def _derive_key(self, key: str = None, key_size: int = 256) -> bytes:
        """
        Derives a key from the provided string or generates one based on the current file path if no key is given.

        :param key: Optional key string to derive a fixed-length key.
        :param key_size: Size of the key to be derived (128, 192, or 256 bits).
        :return: A key of the appropriate length in bytes (16, 24, or 32 bytes).
        """
        if not key:
            key = self.separator

        # Derive a key based on the required size
        if key_size == 128:
            return hashlib.sha256(key.encode()).digest()[:16]  # 16 bytes = 128 bits
        elif key_size == 192:
            return hashlib.sha256(key.encode()).digest()[:24]  # 24 bytes = 192 bits
        elif key_size == 256:
            return hashlib.sha256(key.encode()).digest()[:32]  # 32 bytes = 256 bits

    def encrypt(self, plaintext: str, iv_size: int = 12) -> str:
        """
        Encrypts a plaintext string using AES-GCM.

        :param plaintext: The plaintext string to be encrypted.
        :param iv_size: Size of the Initialization Vector (IV). Defaults to 12 bytes (recommended for GCM mode).
        :return: Encrypted string formatted as "ciphertextΔivΔtag".
        """
        # Generate a random IV (Initialization Vector)
        iv = os.urandom(iv_size)

        # Convert plaintext to bytes
        plaintext_bytes = plaintext.encode()

        # Create AES cipher in GCM mode
        encryptor = Cipher(
            algorithms.AES(self.key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()

        # Encrypt the plaintext
        ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()

        # Return a string combining ciphertext, IV, and authentication tag, separated by 'Δ'
        return f"{ciphertext.hex()}{self.separator}{iv.hex()}{self.separator}{encryptor.tag.hex()}"

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypts an encrypted string using AES-GCM.

        :param encrypted_data: Encrypted string formatted as "ciphertextΔivΔtag".
        :return: Decrypted plaintext string.
        :raises ValueError: If decryption fails (e.g., invalid data or tampered tag).
        """
        try:
            # Split the encrypted string into ciphertext, IV, and tag
            ciphertext_hex, iv_hex, tag_hex = encrypted_data.split(self.separator)
            ciphertext = bytes.fromhex(ciphertext_hex)
            iv = bytes.fromhex(iv_hex)
            tag = bytes.fromhex(tag_hex)

            # Create AES cipher in GCM mode with the provided IV and tag
            decryptor = Cipher(
                algorithms.AES(self.key),
                modes.GCM(iv, tag),
                backend=default_backend()
            ).decryptor()

            # Decrypt the ciphertext
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            # Return the decrypted plaintext as a string
            return plaintext.decode()

        except Exception as e:
            # Raise a more informative error if decryption fails
            raise ValueError(f"Decryption failed: {e}")

