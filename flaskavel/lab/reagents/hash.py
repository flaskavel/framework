import bcrypt

class Hash:

    @staticmethod
    def make(password: str) -> str:
        """
        Hashes the given password using bcrypt.

        :param password: The password to hash.
        :return: The hashed password.
        """
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    @staticmethod
    def check(password: str, hashed: str) -> bool:
        """
        Checks if the given password matches the hashed password.

        :param password: The password to check.
        :param hashed: The hashed password to compare against.
        :return: True if the password matches the hash, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))