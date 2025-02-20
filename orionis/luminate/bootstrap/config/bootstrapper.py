import ast
import importlib
import os
from orionis.luminate.bootstrap.config.register import Register
from orionis.luminate.contracts.bootstrap.bootstrapper_interface import IBootstrapper

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

    findClasses(file_path: str) -> List[str]
        Parses a Python file to extract and return all defined class names.

    autoload(directory: str) -> None
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

    def findClasses(self, file_path: str):
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
        classes = []
        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)

        return classes

    def autoload(self, directory: str = 'config') -> None:
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
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory '{directory}' not found.")

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    file_path = os.path.join(root, file)
                    # Get the class names defined in the file
                    classes = self.findClasses(file_path)

                    if classes:
                        for class_name in classes:
                            # Construct the module path and import the module
                            module_path = root.replace(os.getcwd(), "").replace(os.sep, ".") + "." + file[:-3]
                            module = importlib.import_module(module_path)
                            class_obj = getattr(module, class_name)

                            # Register the class in the container using the Register instance
                            self.register.config(class_obj)
