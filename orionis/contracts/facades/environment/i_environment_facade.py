from abc import ABC, abstractmethod

class IEnv(ABC):

    @abstractmethod
    def _initialize(self, path: str = None):
        """
        Initializes the instance by setting the path to the .env file.
        If no path is provided, defaults to a `.env` file in the current directory.

        Parameters
        ----------
        path : str, optional
            Path to the .env file. Defaults to None.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def unset(self, key: str) -> None:
        """
        Removes an environment variable from the .env file.

        Parameters
        ----------
        key : str
            The key of the environment variable to remove.
        """
        pass

    @abstractmethod
    def all(self) -> dict:
        """
        Retrieves all environment variable values from the .env file.

        Returns
        -------
        dict
            A dictionary of all environment variables and their values.
        """
        pass