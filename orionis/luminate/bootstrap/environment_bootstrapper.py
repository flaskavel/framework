from typing import Dict
from orionis.contracts.bootstrap.i_environment_bootstrapper import IEnvironmentBootstrapper
from orionis.luminate.facades.app import app
from orionis.luminate.services.environment.environment_service import EnvironmentService

class EnvironmentBootstrapper(IEnvironmentBootstrapper):
    """
    A class responsible for loading and managing environment variables from a `.env` file.

    This class implements the `IEnvironment` interface and provides functionality to
    automatically load environment variables from a `.env` file located in the current
    working directory. If the file does not exist, it creates it.

    Attributes
    ----------
    _environment_vars : Dict[str, str]
        A dictionary to store the loaded environment variables.
    path : Path
        The path to the `.env` file.

    Methods
    -------
    __init__()
        Initializes the `EnvironmentBootstrapper` and triggers the autoload process.
    _autoload()
        Loads environment variables from the `.env` file or creates the file if it does not exist.
    """

    def __init__(self) -> None:
        """
        Initializes the `EnvironmentBootstrapper` and triggers the autoload process.

        The `_environment_vars` dictionary is initialized to store environment variables,
        and the `_autoload` method is called to load variables from the `.env` file.
        """
        self._environment_vars: Dict[str, str] = {}
        self._autoload()

    def _autoload(self) -> None:
        """
        Loads environment variables from the `.env` file or creates the file if it does not exist.

        This method checks if the `.env` file exists in the current working directory.
        If the file does not exist, it creates an empty `.env` file. If the file exists,
        it loads the environment variables into the `_environment_vars` dictionary.
        """
        environment_service : EnvironmentService = app(EnvironmentService)
        self._environment_vars = environment_service.all()

    def get(self, key: str = None) -> str:
        """
        Retrieves the value of an environment variable by its key.

        Parameters
        ----------
        key : str
            The key of the environment variable to retrieve.

        Returns
        -------
        str
            The value of the environment variable.

        Raises
        ------
        KeyError
            If the environment variable does not exist.
        """

        if not key:
            return self._environment_vars

        if key not in self._environment_vars:
            raise KeyError(f"Environment variable {key} not found")

        return self._environment_vars[key]