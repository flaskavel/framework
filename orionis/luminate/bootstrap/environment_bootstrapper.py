import ast
import os
from pathlib import Path
from typing import Dict
from dotenv import dotenv_values
from orionis.contracts.bootstrap.i_environment_bootstrapper import IEnvironmentBootstrapper
from orionis.luminate.bootstrap.exception_bootstrapper import BootstrapRuntimeError

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

        Raises
        ------
        PermissionError
            If the `.env` file cannot be created or read due to insufficient permissions.
        """
        # Set the path to the `.env` file
        path: Path = Path(os.getcwd()) / ".env"

        # Create the `.env` file if it does not exist
        if not path.exists():
            try:
                path.touch()  # Create an empty `.env` file if it does not exist
            except PermissionError as e:
                raise PermissionError(f"Cannot create `.env` file at {path}: {str(e)}")

        try:
            all_vars = dotenv_values(path)
            for key, value in all_vars.items():
                self._environment_vars[key] = self._parse_value(value)
        except Exception as e:
            raise BootstrapRuntimeError(f"Error loading environment variables from {path}: {str(e)}")

    def _parse_value(self, value):
        """
        Parse and convert a string value into its appropriate Python data type.

        This function handles conversion for common types such as `None`, booleans (`True`/`False`),
        integers, and Python literals (e.g., lists, dictionaries). If the value cannot be parsed
        into a specific type, it is returned as-is.

        Parameters
        ----------
        value : str or None
            The value to be parsed. If `None`, it is returned as `None`.

        Returns
        -------
        any
            The parsed value. Possible return types include:
            - `None` if the value is empty, `None`, `'None'`, or `'null'`.
            - `bool` if the value is `'True'`, `'true'`, `'False'`, or `'false'`.
            - `int` if the value is a digit string (e.g., `'123'`).
            - Python literals (e.g., lists, dictionaries) if the value can be evaluated as such.
            - The original value if no conversion is applicable.
        """
        # Strip leading and trailing whitespace from the value
        value = str(value).strip() if value is not None else None

        # Parse common types and Python literals
        if not value or value.lower() in {'none', 'null'}:
            return None
        if value.lower() in {'true', 'false'}:
            return value.lower() == 'true'
        if value.isdigit():
            return int(value)

        # Attempt to parse Python literals (e.g., lists, dictionaries)
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value

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