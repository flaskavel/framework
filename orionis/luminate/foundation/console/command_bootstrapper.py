import pathlib
import importlib
import inspect
from typing import Any, Callable, Dict, List
from orionis.luminate.contracts.foundation.console.i_command_bootstrapper import ICommandsBootstrapper
from orionis.luminate.foundation.exceptions.exception_bootstrapper import BootstrapRuntimeError
from orionis.luminate.console.base.command import BaseCommand

class CommandsBootstrapper(ICommandsBootstrapper):
    """
    A class responsible for loading and registering console commands dynamically.

    This class scans specified directories for Python files, imports them, and registers
    command classes that inherit from `BaseCommand`. It ensures that commands are loaded
    only once and provides methods to access and manage them.

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

    def __init__(self) -> None:
        """
        Initializes the `CommandsBootstrapper` and triggers the autoload process.

        The `_commands` dictionary is initialized to store command data, and the
        `_autoload` method is called to load commands from the specified directories.
        """
        self._commands: Dict[str, Dict[str, Any]] = {}
        self._autoload()

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
        base_path = pathlib.Path.cwd()

        # Define the directories to scan for commands
        command_dirs = [
            base_path / "app" / "console" / "commands",  # Developer-defined commands
            pathlib.Path(__file__).resolve().parent.parent.parent / "console" / "commands"  # Core commands
        ]

        for cmd_dir in command_dirs:
            if not cmd_dir.is_dir():
                continue

            for file_path in cmd_dir.rglob("*.py"):
                if file_path.name == "__init__.py":
                    continue

                module_path = ".".join(file_path.relative_to(base_path).with_suffix("").parts)

                # Remove 'site-packages.' prefix if present
                if 'site-packages.' in module_path:
                    module_path = module_path.split('site-packages.')[1]

                try:
                    module = importlib.import_module(module_path.strip())

                    # Find and register command classes
                    for name, concrete in inspect.getmembers(module, inspect.isclass):
                        if issubclass(concrete, BaseCommand) and concrete is not BaseCommand:
                            self._register(concrete)
                except Exception as e:
                    raise BootstrapRuntimeError(f"Error loading {module_path}") from e

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
        if not isinstance(concrete, type):
            raise TypeError(f"Expected a class, but got {type(concrete).__name__}.")

        # Validate 'signature' attribute
        if not hasattr(concrete, 'signature') or not isinstance(concrete.signature, str):
            raise ValueError(f"Class {concrete.__name__} must have a 'signature' attribute as a string.")

        signature = concrete.signature.strip()

        # Validate signature format
        if not signature or ' ' in signature or not all(c.isalnum() or c == ":" for c in signature):
            raise ValueError(f"Invalid signature format: '{signature}'. Only letters, numbers, and ':' are allowed, with no spaces.")

        # Validate 'description' attribute
        if not hasattr(concrete, 'description') or not isinstance(concrete.description, str):
            raise ValueError(f"Class {concrete.__name__} must have a 'description' attribute as a string.")

        description = concrete.description.strip()

        # Validate 'handle' method
        if not hasattr(concrete, 'handle') or not callable(getattr(concrete, 'handle')):
            raise ValueError(f"Class {concrete.__name__} must implement a 'handle' method.")

        # Validate 'arguments' method (optional)
        arguments: List[Any] = []
        if hasattr(concrete, 'arguments') and callable(getattr(concrete, 'arguments')):
            arguments = concrete().arguments()

        # Validate inheritance from 'BaseCommand'
        if not issubclass(concrete, BaseCommand):
            raise TypeError(f"Class {concrete.__name__} must inherit from 'BaseCommand'.")

        # Ensure the command signature is unique
        if signature in self._commands:
            raise ValueError(f"Command '{signature}' is already registered. Please ensure signatures are unique.")

        # Register the command
        self._commands[signature] = {
            'concrete': concrete,
            'arguments': arguments,
            'description': description,
            'signature': signature
        }

    def get(self, signature: str = None) -> Dict[str, Any]:
        """
        Retrieves a registered command by its signature.

        Parameters
        ----------
        signature : str
            The command signature to retrieve.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing the command class, arguments, description, and signature.

        Raises
        ------
        KeyError
            If the command signature is not found.
        """
        if signature is None:
            return self._commands
        if signature not in self._commands:
            raise KeyError(f"Command '{signature}' not found.")
        return self._commands[signature]