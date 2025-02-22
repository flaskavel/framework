from abc import ABC, abstractmethod
from typing import Any, Optional

class IEnvironmentBootstrapper(ABC):
    """
    Attributes
    ----------
    _environment_vars : Dict[str, str]
        A dictionary to store the loaded environment variables.
    path : Path
        The path to the `.env` file.

    Methods
    -------
    _autoload()
        Loads environment variables from the `.env` file or creates the file if it does not exist.
    """

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