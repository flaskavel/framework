from abc import ABC, abstractmethod
from typing import Any

class IBootstrapper(ABC):

    @abstractmethod
    def _autoload(self) -> None:
        """
        Loads environment variables from the `.env` file or creates the file if it does not exist.

        This method checks if the `.env` file exists in the current working directory.
        If the file does not exist, it creates an empty `.env` file. If the file exists,
        it loads the environment variables into the `_environment_vars` dictionary.

        Raises
        ------
        PermissionError
            If the `.env` file cannot be created or read due to insufficient permissions.
        """
        pass

    def get(self, *args, **kwargs) -> Any:
        """
        Retrieves the value of an environment variable.

        Parameters
        ----------
        key : str
            The name of the environment variable.

        Returns
        -------
        str
            The value of the environment variable.

        Raises
        ------
        KeyError
            If the environment variable does not exist.
        """
        pass