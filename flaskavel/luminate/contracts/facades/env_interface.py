from abc import ABC, abstractmethod
from typing import Optional, Dict

class IEnv(ABC):
    """
    Interface for managing environment variables from a .env file.
    """

    @abstractmethod
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Retrieve the value of an environment variable.

        Parameters
        ----------
        key : str
            The key of the environment variable.
        default : Optional[str], optional
            Default value if the key does not exist, by default None.

        Returns
        -------
        Optional[str]
            The value of the environment variable or the default value.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        """
        Set the value of an environment variable in the .env file.

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
        Remove an environment variable from the .env file.

        Parameters
        ----------
        key : str
            The key of the environment variable to remove.
        """
        pass

    @abstractmethod
    def all(self) -> Dict[str, str]:
        """
        Retrieve all environment variable values from the .env file.

        Returns
        -------
        Dict[str, str]
            A dictionary of all environment variables and their values.
        """
        pass
