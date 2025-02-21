import importlib
import pathlib
from orionis.luminate.bootstrap.config.register import Register
from orionis.luminate.contracts.bootstrap.config.bootstrapper_interface import IBootstrapper

class Bootstrapper(IBootstrapper):
    """
    Manages the automatic loading and registration of configuration classes
    from Python files located in a specified directory.

    The `Bootstrapper` class scans directories for Python files and dynamically
    imports them to find configuration classes. Once found, the classes are
    registered using the provided `Register` instance.

    Attributes
    ----------
    register : Register
        An instance of the `Register` class used to register configuration classes.

    Methods
    -------
    __init__(register: Register) -> None
        Initializes the `Bootstrapper` with a `Register` instance.

    _autoload(directory: str) -> None
        Scans a directory for Python files, imports them, finds configuration classes,
        and registers them using the `Register` instance.
    """

    def __init__(self, register: Register) -> None:
        """
        Initializes the `Bootstrapper` with a `Register` instance.

        Parameters
        ----------
        register : Register
            An instance of the `Register` class used to register configuration classes.
        """
        self.register = register
        self._autoload()

    def _autoload(self, directory: str = 'config') -> None:
        """
        Automatically registers configuration classes found in a given directory.

        This method walks through the specified directory, imports all Python files,
        and scans for class definitions. If a class is found, it is registered using
        the `Register` instance. Only classes defined in Python files (excluding
        `__init__.py`) are considered.

        Parameters
        ----------
        directory : str
            The directory to scan for Python configuration files.

        Raises
        ------
        FileNotFoundError
            If the provided directory does not exist.
        """
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
                    self.register.config(getattr(module, "Config"))
            except Exception as e:
                raise RuntimeError(f"Error loading module {module_path}") from e

