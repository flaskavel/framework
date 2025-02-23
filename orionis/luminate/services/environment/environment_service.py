import os
from pathlib import Path
from dotenv import set_key, unset_key, dotenv_values
from orionis.contracts.services.environment.i_environment_service import IEnvironmentService

class EnvironmentService(IEnvironmentService):

    def __init__(self, path: str = None):

        """
        Initializes the EnvironmentService instance.

        Parameters
        ----------
        path : str, optional
            The path to the .env file. Defaults to None.
        """
        self._initialize(path)

    def _initialize(self, path: str = None):
        """
        Initializes the instance by setting the path to the .env file.
        If no path is provided, defaults to a `.env` file in the current directory.

        Parameters
        ----------
        path : str, optional
            Path to the .env file. Defaults to None.
        """
        # Set the path to the .env file
        self.path = Path(path) if path else Path(os.getcwd()) / ".env"

        # Create the .env file if it does not exist
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
        # Get the value from the .env file
        value = dotenv_values(self.path).get(key)

        # Return the value or the default value
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
        # Set the value in the .env file
        set_key(str(self.path), key, value)

    def unset(self, key: str) -> None:
        """
        Removes an environment variable from the .env file.

        Parameters
        ----------
        key : str
            The key of the environment variable to remove.
        """
        # Remove the key from the .env file
        unset_key(str(self.path), key)

    def all(self) -> dict:
        """
        Retrieves all environment variable values from the .env file.

        Returns
        -------
        dict
            A dictionary of all environment variables and their values.
        """
        # Return all environment variables
        return dotenv_values(self.path)