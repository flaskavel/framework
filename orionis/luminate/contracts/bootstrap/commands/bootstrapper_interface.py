from abc import ABC, abstractmethod

class IBootstrapper(ABC):
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

    @abstractmethod
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
        pass