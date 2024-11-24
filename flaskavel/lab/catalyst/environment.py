import os
import threading
from dotenv import get_key, set_key, unset_key, dotenv_values

class _Environment:
    """
    Singleton class to manage environment variables from a .env file.
    Ensures a single instance handles environment variable access,
    modification, and deletion.
    """

    # Singleton instance
    _instance = None

    # Thread lock to control instance creation
    _lock = threading.Lock()

    def __new__(cls, path: str = None):
        """
        Creates or returns the singleton instance. Uses a thread lock to ensure
        thread-safe initialization of the instance.

        Args:
            path (str, optional): Path to the .env file. Defaults to None.

        Returns:
            _Environment: The singleton instance of _Environment.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(_Environment, cls).__new__(cls)
                cls._instance._initialize(path)
        return cls._instance

    def _initialize(self, path: str = None):
        """
        Initializes the instance by setting the path to the .env file.

        Args:
            path (str, optional): Path to the .env file. If not provided,
                                  defaults to a relative path to locate .env.
        """
        self.path = path

        # This block should never be executed. Ensure that 'self.path' always has a valid value.
        if not self.path:

            # Assign the value of 'self.path' to the '.env' file located at a relative path.
            self.path = os.path.join(__file__, '../../../../../../../.env')

    def get(self, key: str, default=None):
        """
        Retrieves the value of an environment variable.

        Args:
            key (str): The key of the environment variable.
            default: Default value if the key does not exist.

        Returns:
            str: The value of the environment variable or the default value.
        """
        if key not in dotenv_values(dotenv_path=self.path):
            return default

        return get_key(dotenv_path=self.path, key_to_get=key)

    def set(self, key: str, value: str):
        """
        Sets the value of an environment variable in the .env file.

        Args:
            key (str): The key of the environment variable.
            value (str): The value to set.

        Returns:
            None
        """
        set_key(dotenv_path=self.path, key_to_set=str(key), value_to_set=str(value))

    def unset(self, key: str):
        """
        Removes an environment variable from the .env file.

        Args:
            key (str): The key of the environment variable to remove.

        Returns:
            None
        """
        unset_key(dotenv_path=self.path, key_to_unset=str(key))

    def get_values(self):
        """
        Retrieves all environment variable values from the .env file.

        Returns:
            dict: A dictionary of all environment variables and their values.
        """
        return dotenv_values(dotenv_path=self.path)

    def get_path(self):
        """
        Retrieves the path of the .env file.

        Returns:
            str: The path of the .env file.
        """
        return self.path
