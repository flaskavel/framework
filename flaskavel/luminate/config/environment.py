import os
import threading
from pathlib import Path
from dotenv import set_key, unset_key, dotenv_values
from flaskavel.luminate.contracts.config.environment_interface import IEnvironment

class Environment(IEnvironment):
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
        Creates or returns the singleton instance.
        Ensures thread-safe initialization using a lock.

        Parameters
        ----------
        path : str, optional
            Path to the .env file. Defaults to None.

        Returns
        -------
        _Environment
            The singleton instance of _Environment.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize(path)
        return cls._instance

    def _initialize(self, path: str = None):
        """
        Initializes the instance by setting the path to the .env file.
        If no path is provided, defaults to a `.env` file in the current directory.

        Parameters
        ----------
        path : str, optional
            Path to the .env file. Defaults to None.
        """
        self.path = Path(path) if path else Path(os.getcwd()) / ".env"

        # Ensure the .env file exists
        if not self.path.exists():
            self.path.touch()

    def get(self, key: str, default=None) -> str:
        """
        Retrieves the value of an environment variable from the .env file
        or from system environment variables if not found.

        Parameters
        ----------
        key : str
            The key of the environment variable.
        default : optional
            Default value if the key does not exist. Defaults to None.

        Returns
        -------
        str
            The value of the environment variable or the default value.
        """
        value = dotenv_values(self.path).get(key)
        return value if value is not None else os.getenv(key, default)

    def set(self, key: str, value: str) -> None:
        """
        Sets the value of an environment variable in the .env file.

        Parameters
        ----------
        key : str
            The key of the environment variable.
        value : str
            The value to set.
        """
        set_key(str(self.path), key, value)

    def unset(self, key: str) -> None:
        """
        Removes an environment variable from the .env file.

        Parameters
        ----------
        key : str
            The key of the environment variable to remove.
        """
        unset_key(str(self.path), key)

    def all(self) -> dict:
        """
        Retrieves all environment variable values from the .env file.

        Returns
        -------
        dict
            A dictionary of all environment variables and their values.
        """
        return dotenv_values(self.path)