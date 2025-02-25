import importlib
import pathlib
from dataclasses import asdict
from typing import Any, Dict
from orionis.luminate.contracts.foundation.config.i_config_bootstrapper import IConfigBootstrapper
from orionis.luminate.contracts.config.i_config import IConfig
from orionis.luminate.foundation.exceptions.exception_bootstrapper import BootstrapRuntimeError

class ConfigBootstrapper(IConfigBootstrapper):
    """
    A class responsible for loading and registering application configurations dynamically.

    This class scans a specified directory for Python files, imports them, and registers
    configuration classes that inherit from `IConfig`. It ensures that configurations
    are loaded only once and provides methods to access and modify them.

    Attributes
    ----------
    _config : Dict[str, Any]
        A dictionary to store registered configuration sections and their data.

    Methods
    -------
    __init__()
        Initializes the `ConfigBootstrapper` and triggers the autoload process.
    _autoload()
        Scans the configuration directory and loads configuration classes.
    _set(concrete: Any, section: str)
        Validates and registers a configuration class.
    _parse(data: Any) -> Dict[str, Any]
        Converts the 'config' attribute of a class into a dictionary.
    _register(section: str, data: Dict[str, Any])
        Registers a configuration section.
    set(key: str, value: Any)
        Dynamically sets a configuration value using dot notation.
    get(key: str, default: Optional[Any] = None) -> Any
        Retrieves a configuration value using dot notation.
    """

    def __init__(self) -> None:
        """
        Initializes the `ConfigBootstrapper` and triggers the autoload process.

        The `_config` dictionary is initialized to store configuration data, and the
        `_autoload` method is called to load configurations from the default directory.
        """
        self._config: Dict[str, Any] = {}
        self._autoload()

    def _autoload(self) -> None:
        """
        Scans the configuration directory and loads configuration classes.

        This method searches for Python files in the specified directory, imports them,
        and registers any class named `Config` that inherits from `IConfig`.

        Raises
        ------
        FileNotFoundError
            If the configuration directory does not exist.
        BootstrapRuntimeError
            If there is an error loading a module.
        """
        directory = "config"
        base_path = pathlib.Path(directory).resolve()

        if not base_path.exists():
            raise FileNotFoundError(f"Directory {directory} does not exist.")

        for file_path in base_path.rglob("*.py"):
            if file_path.name == "__init__.py":
                continue

            module_path = ".".join(file_path.relative_to(base_path).with_suffix("").parts)

            try:
                module = importlib.import_module(f"{directory}.{module_path}")
                if hasattr(module, "Config"):
                    self._set(
                        concrete=getattr(module, "Config"),
                        section=module_path
                    )
            except Exception as e:
                raise BootstrapRuntimeError(f"Error loading module {module_path}") from e

    def _set(self, concrete: Any, section: str) -> None:
        """
        Validates and registers a configuration class.

        This method ensures that the provided class is valid (inherits from `IConfig`
        and has a `config` attribute) and registers it in the `_config` dictionary.

        Parameters
        ----------
        concrete : Any
            The configuration class to register.
        section : str
            The section name under which the configuration will be registered.

        Raises
        ------
        TypeError
            If the input is not a class or does not inherit from `IConfig`.
        ValueError
            If the class does not have a `config` attribute.
        """
        if not isinstance(concrete, type):
            raise TypeError(f"Expected a class, but got {type(concrete).__name__}.")

        if not hasattr(concrete, "config"):
            raise ValueError(f"Class {concrete.__name__} must have a 'config' attribute.")

        if not issubclass(concrete, IConfig):
            raise TypeError(f"Class {concrete.__name__} must inherit from 'IConfig'.")

        self._register(
            section=section,
            data=self._parse(concrete.config)
        )

    def _parse(self, data: Any) -> Dict[str, Any]:
        """
        Converts the 'config' attribute of a class into a dictionary.

        If the input is already a dictionary, it is returned as-is. If the input is a
        dataclass, it is converted to a dictionary using `asdict`.

        Parameters
        ----------
        data : Any
            The data to convert into a dictionary.

        Returns
        -------
        Dict[str, Any]
            The converted dictionary.

        Raises
        ------
        TypeError
            If the data cannot be converted to a dictionary.
        """
        if isinstance(data, dict):
            return data
        try:
            return asdict(data)
        except TypeError as e:
            raise TypeError(f"Error: The 'config' attribute could not be converted to a dictionary. {str(e)}")

    def _register(self, section: str, data: Dict[str, Any]) -> None:
        """
        Registers a configuration section.

        Parameters
        ----------
        section : str
            The name of the configuration section.
        data : Dict[str, Any]
            The configuration data to register.

        Raises
        ------
        ValueError
            If the section is already registered.
        """
        if section in self._config:
            raise ValueError(f"Configuration section '{section}' is already registered.")
        self._config[section] = data

    def get(self, key: str = None, default: Any = None) -> Any:
        """
        Retrieves configuration data.

        If a key is provided, it retrieves the value associated with the key using dot notation.
        If no key is provided, it returns the entire configuration dictionary.

        Parameters
        ----------
        key : str, optional
            The key to retrieve the value for, using dot notation (default is None).
        default : Any, optional
            The default value to return if the key is not found (default is None).

        Returns
        -------
        Any
            The configuration value associated with the key, or the entire configuration dictionary
            if no key is provided. If the key is not found, returns the default value.

        Raises
        ------
        KeyError
            If the key is not found and no default value is provided.
        """
        if key is None:
            return self._config

        keys = key.split('.')
        value = self._config

        try:
            for k in keys:
                value = value[k]
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f"Key '{key}' not found in configuration.")

        return value