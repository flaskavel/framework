from flaskavel.lab.catalyst.encryption import _Encryption

class Crypt:
    """
    Provides static methods to encrypt and decrypt values using AES-GCM encryption.
    """

    @staticmethod
    def encrypt(value: str, key=None) -> str:
        """
        Encrypts a given plaintext using AES-GCM encryption.

        :param value: The plaintext value to be encrypted.
        :return: Encrypted string in the format "ciphertextΔivΔtag".
        """
        return _Encryption(key=key).encrypt(plaintext=value)

    @staticmethod
    def decrypt(value: str, key=None) -> str:
        """
        Decrypts a given encrypted string using AES-GCM decryption.

        :param value: The encrypted string to be decrypted.
        :return: Decrypted plaintext string.
        """
        return _Encryption(key=key).decrypt(encrypted_data=value)


