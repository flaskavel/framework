from abc import ABC, abstractmethod

class IBootstrapper(ABC):
    """
    Interface for managing the automatic loading and registration of configuration
    classes from Python files located in a specified directory.

    The `IBootstrapper` interface defines methods for scanning directories for
    Python files and dynamically importing them to find configuration classes.
    Implementations of this interface should provide the logic for registering
    the found classes using a `Register` instance.

    Methods
    -------
    autoload(directory: str) -> None
        Scans a directory for Python files, imports them, finds configuration classes,
        and registers them using the `Register` instance.
    """

    @abstractmethod
    def _autoload(self, directory: str) -> None:
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
        pass