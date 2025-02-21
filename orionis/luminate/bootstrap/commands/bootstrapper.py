import pathlib
import importlib
import inspect
from orionis.luminate.bootstrap.cli_exception import BootstrapRuntimeError
from orionis.luminate.bootstrap.commands.register import Register
from orionis.luminate.console.base.command import BaseCommand
from orionis.luminate.contracts.bootstrap.commands.bootstrapper_interface import IBootstrapper

class Bootstrapper(IBootstrapper):
    """
    Manages the automatic loading and registration of command classes
    from Python files located in predefined directories.

    The `Bootstrapper` class scans specific directories for Python files, dynamically
    imports them, and registers classes that inherit from `BaseCommand`.

    Attributes
    ----------
    register : Register
        An instance of the `Register` class used to register command classes.

    Methods
    -------
    __init__(register: Register) -> None
        Initializes the `Bootstrapper` with a `Register` instance and triggers autoloading.
    _autoload() -> None
        Scans predefined directories for Python files, dynamically imports modules,
        and registers classes that extend `BaseCommand`.
    """

    def __init__(self, register: Register) -> None:
        """
        Initializes the `Bootstrapper` with a `Register` instance and triggers autoloading.

        Parameters
        ----------
        register : Register
            An instance of the `Register` class used to register command classes.
        """
        self.register = register
        self._autoload()

    def _autoload(self) -> None:
        """
        Autoloads command modules from specified directories and registers command classes.

        This method searches for Python files in the predefined command directories,
        dynamically imports the modules, and registers classes that inherit from `BaseCommand`.

        The command directories searched are:
        - `app/console/commands` relative to the current working directory.
        - `console/commands` relative to the parent directory of the current file.

        It skips `__init__.py` files and ignores directories that do not exist.

        Raises
        ------
        BootstrapRuntimeError
            If an error occurs while loading a module.
        """

        # Define the base project path
        base_path = pathlib.Path.cwd()

        # Define the command directories to search
        command_dirs = [
            base_path / "app" / "console" / "commands",
            pathlib.Path(__file__).resolve().parent.parent / "console" / "commands"
        ]

        # Iterate over each command directory
        for cmd_dir in command_dirs:

            # Skip if the directory does not exist
            if not cmd_dir.is_dir():
                continue

            # Iterate over Python files in the directory (recursive search)
            for file_path in cmd_dir.rglob("*.py"):

                # Skip `__init__.py` files
                if file_path.name == "__init__.py":
                    continue

                # Convert file path to a Python module import path
                module_path = ".".join(file_path.relative_to(base_path).with_suffix("").parts)

                try:
                    # Dynamically import the module
                    module = importlib.import_module(module_path)

                    # Find classes that inherit from `BaseCommand`
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, BaseCommand) and obj is not BaseCommand:
                            # Register the class
                            self.register.command(obj)

                except Exception as e:
                    raise BootstrapRuntimeError(f"Error loading {module_path}") from e