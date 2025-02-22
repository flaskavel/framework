import os
import inspect
import importlib
from enum import Enum
from typing import Any, List, Optional
from orionis.contracts.support.i_reflection import IReflection

class Reflection(IReflection):
    """
    The Reflection class dynamically loads a class from a module and inspects its attributes,
    methods, properties, and other properties at runtime. It supports checking the existence of
    classes, methods, properties, constants, and can instantiate classes if they are not abstract.

    Attributes
    ----------
    classname : str, optional
        The name of the class to reflect upon. Default is None.
    module_name : str, optional
        The name of the module where the class is defined. Default is None.
    cls : type, optional
        The class object after it has been imported and assigned. Default is None.
    """

    def __init__(self, target: Optional[Any] = None, module: Optional[str] = None):
        """
        Initializes the Reflection instance with an optional class name, module name, or instance.

        Parameters
        ----------
        target : Any, optional
            The class name as a string, the class type, or an instance of the class. Default is None.
        module : str, optional
            The name of the module where the class is defined. Default is None.
        """
        self.classname = None
        self.module_name = module
        self.cls = None

        if isinstance(target, str):
            self.classname = target
        elif isinstance(target, type):
            self.cls = target
            self.classname = target.__name__
        elif target is not None:
            self.cls = target.__class__
            self.classname = self.cls.__name__

        if self.module_name and not self.cls:
            self.safeImport()

    def safeImport(self):
        """
        Safely imports the specified module and assigns the class object if a classname is provided.

        This method raises a ValueError if the module cannot be imported or if the class does not exist
        within the module.

        Raises
        ------
        ValueError
            If the module cannot be imported or the class does not exist in the module.
        """
        try:
            module = importlib.import_module(self.module_name)
            if self.classname:
                self.cls = getattr(module, self.classname, None)
                if self.cls is None:
                    raise ValueError(f"Class '{self.classname}' not found in module '{self.module_name}'.")
        except ImportError as e:
            raise ValueError(f"Error importing module '{self.module_name}': {e}")

    def getFile(self) -> str:
        """
        Retrieves the file path where the class is defined.

        Returns
        -------
        str
            The file path if the class is found, otherwise raises an error.

        Raises
        ------
        ValueError
            If the class has not been loaded yet.
        """
        if not self.cls:
            raise ValueError("Class not loaded. Use 'safeImport()' first.")
        return inspect.getfile(self.cls)

    def hasClass(self) -> bool:
        """
        Checks whether the class object is available.

        Returns
        -------
        bool
            True if the class is loaded, False otherwise.
        """
        return self.cls is not None

    def hasMethod(self, method_name: str) -> bool:
        """
        Checks whether the specified method exists in the class.

        Parameters
        ----------
        method_name : str
            The name of the method to check.

        Returns
        -------
        bool
            True if the method exists, False otherwise.
        """
        return hasattr(self.cls, method_name) if self.cls else False

    def hasProperty(self, prop: str) -> bool:
        """
        Checks whether the specified property exists in the class.

        Parameters
        ----------
        prop : str
            The name of the property to check.

        Returns
        -------
        bool
            True if the property exists, False otherwise.
        """
        return hasattr(self.cls, prop) if self.cls else False

    def hasConstant(self, constant: str) -> bool:
        """
        Checks whether the specified constant exists in the class.

        Parameters
        ----------
        constant : str
            The name of the constant to check.

        Returns
        -------
        bool
            True if the constant exists, False otherwise.
        """
        return hasattr(self.cls, constant) if self.cls else False

    def getAttributes(self) -> List[str]:
        """
        Retrieves a list of all attributes (including methods and properties) of the class.

        Returns
        -------
        list
            A list of attribute names in the class.
        """
        return dir(self.cls) if self.cls else []

    def getConstructor(self):
        """
        Retrieves the constructor (__init__) of the class.

        Returns
        -------
        function or None
            The constructor method if available, otherwise None.
        """
        return self.cls.__init__ if self.cls else None

    def getDocComment(self) -> Optional[str]:
        """
        Retrieves the docstring of the class.

        Returns
        -------
        str or None
            The docstring of the class if available, otherwise None.
        """
        if not self.cls:
            raise ValueError("Class not loaded. Use 'safeImport()' first.")
        return self.cls.__doc__

    def getFileName(self, remove_extension: bool = False) -> str:
        """
        Retrieves the file name where the class is defined, the same as `get_file()`.

        Parameters
        ----------
        remove_extension : bool, optional
            If True, the file extension will be removed from the filename. Default is False.

        Returns
        -------
        str
            The file name of the class definition.
        """
        file_name = os.path.basename(self.getFile())
        if remove_extension:
            file_name = os.path.splitext(file_name)[0]
        return file_name

    def getMethod(self, method_name: str):
        """
        Retrieves the specified method from the class.

        Parameters
        ----------
        method_name : str
            The name of the method to retrieve.

        Returns
        -------
        function or None
            The method if it exists, otherwise None.
        """
        return getattr(self.cls, method_name, None) if self.cls else None

    def getMethods(self) -> List[str]:
        """
        Retrieves a list of all methods in the class.

        Returns
        -------
        list
            A list of method names in the class.
        """
        return [method for method, _ in inspect.getmembers(self.cls, predicate=inspect.isfunction)] if self.cls else []

    def getName(self) -> str:
        """
        Retrieves the name of the class.

        Returns
        -------
        str or None
            The name of the class if available, otherwise None.
        """
        return self.cls.__name__ if self.cls else None

    def getParentClass(self) -> Optional[tuple]:
        """
        Retrieves the parent classes (base classes) of the class.

        Returns
        -------
        tuple or None
            A tuple of base classes if available, otherwise None.
        """
        return self.cls.__bases__ if self.cls else None

    def getProperties(self) -> List[str]:
        """
        Retrieves a list of all properties of the class.

        Returns
        -------
        list
            A list of property names in the class.
        """
        return [name for name, value in inspect.getmembers(self.cls, lambda x: isinstance(x, property))] if self.cls else []

    def getProperty(self, prop: str):
        """
        Retrieves the specified property from the class.

        Parameters
        ----------
        prop : str
            The name of the property to retrieve.

        Returns
        -------
        property or None
            The property if it exists, otherwise None.
        """
        return getattr(self.cls, prop, None) if self.cls else None

    def isAbstract(self) -> bool:
        """
        Checks whether the class is abstract.

        Returns
        -------
        bool
            True if the class is abstract, False otherwise.
        """
        return hasattr(self.cls, '__abstractmethods__') and bool(self.cls.__abstractmethods__) if self.cls else False

    def isEnum(self) -> bool:
        """
        Checks whether the class is an enumeration.

        Returns
        -------
        bool
            True if the class is a subclass of Enum, False otherwise.
        """
        return self.cls is not None and isinstance(self.cls, type) and issubclass(self.cls, Enum)

    def isSubclassOf(self, parent: type) -> bool:
        """
        Checks whether the class is a subclass of the specified parent class.

        Parameters
        ----------
        parent : type
            The parent class to check against.

        Returns
        -------
        bool
            True if the class is a subclass of the parent, False otherwise.
        """
        return self.cls is not None and issubclass(self.cls, parent)

    def isInstanceOf(self, instance: Any) -> bool:
        """
        Checks whether the class is an instance of the specified class.

        Parameters
        ----------
        parent : type
            The class to check against.

        Returns
        -------
        bool
            True if the class is a subclass of the parent, False otherwise.
        """
        return self.cls is not None and isinstance(instance, self.cls)

    def isIterable(self) -> bool:
        """
        Checks whether the class is iterable.

        Returns
        -------
        bool
            True if the class is iterable, False otherwise.
        """
        return hasattr(self.cls, '__iter__') if self.cls else False

    def isInstantiable(self) -> bool:
        """
        Checks whether the class can be instantiated.

        Returns
        -------
        bool
            True if the class is callable and not abstract, False otherwise.
        """
        return self.cls is not None and callable(self.cls) and not self.isAbstract()

    def newInstance(self, *args, **kwargs):
        """
        Creates a new instance of the class if it is instantiable.

        Parameters
        ----------
        args : tuple
            Arguments to pass to the class constructor.
        kwargs : dict
            Keyword arguments to pass to the class constructor.

        Returns
        -------
        object
            A new instance of the class.

        Raises
        ------
        TypeError
            If the class is not instantiable.
        """
        if self.isInstantiable():
            return self.cls(*args, **kwargs)
        raise TypeError(f"Cannot instantiate class '{self.classname}'. It may be abstract or not callable.")

    def __str__(self) -> str:
        """
        Returns a string representation of the Reflection instance.

        Returns
        -------
        str
            A string describing the class and module.
        """
        status = "loaded" if self.cls else "not loaded"
        return f"<Orionis Reflection class '{self.classname}' in module '{self.module_name}' ({status})>"