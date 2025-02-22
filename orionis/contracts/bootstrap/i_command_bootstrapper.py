from abc import ABC, abstractmethod
from typing import Any, Callable, Dict

class ICommandsBootstrapper(ABC):
    """
    Attributes
    ----------
    _commands : Dict[str, Dict[str, Any]]
        A dictionary to store registered commands, where the key is the command signature
        and the value is a dictionary containing the command class, arguments, description,
        and signature.

    Methods
    -------
    __init__()
        Initializes the `CommandsBootstrapper` and triggers the autoload process.
    _autoload()
        Scans the command directories and loads command classes.
    _register(concrete: Callable[..., Any])
        Validates and registers a command class.
    """

    @abstractmethod
    def _autoload(self) -> None:
        """
        Scans the command directories and loads command classes.

        This method searches for Python files in the specified directories, imports them,
        and registers any class that inherits from `BaseCommand`.

        Raises
        ------
        BootstrapRuntimeError
            If there is an error loading a module.
        """
        pass

    @abstractmethod
    def _register(self, concrete: Callable[..., Any]) -> None:
        """
        Validates and registers a command class.

        This method ensures that the provided class is valid (inherits from `BaseCommand`,
        has a `signature`, `description`, and `handle` method) and registers it in the
        `_commands` dictionary.

        Parameters
        ----------
        concrete : Callable[..., Any]
            The command class to register.

        Raises
        ------
        TypeError
            If the input is not a class or does not inherit from `BaseCommand`.
        ValueError
            If the class does not have required attributes or methods.
        """
        pass