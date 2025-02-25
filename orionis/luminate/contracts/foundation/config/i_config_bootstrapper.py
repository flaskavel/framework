from abc import ABC, abstractmethod
from typing import Any, Dict

class IConfigBootstrapper(ABC):
    """
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

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def _parse(data: Any) -> Dict[str, Any]:
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass