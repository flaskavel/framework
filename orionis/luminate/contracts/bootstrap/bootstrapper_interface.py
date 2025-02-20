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
    findClasses(file_path: str) -> List[str]
        Parses a Python file to extract and return all defined class names.

    autoload(directory: str) -> None
        Scans a directory for Python files, imports them, finds configuration classes,
        and registers them using the `Register` instance.
    """

    @abstractmethod
    def _definitions(self, file_path: str):
        """
        Parses a Python file to extract and return all defined class names.

        This method opens the file at the given path, parses it using the Abstract
        Syntax Tree (AST) module to extract class definitions, and returns a
        list of class names found within the file.

        Parameters
        ----------
        file_path : str
            The path to the Python file to parse.

        Returns
        -------
        List[str]
            A list of class names defined in the provided Python file.
        """
        pass

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