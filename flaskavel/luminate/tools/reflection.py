import inspect
import importlib
from enum import Enum
from flaskavel.luminate.contracts.tools.reflection_interface import IReflection

class Reflection(IReflection):
    """
    The Reflection class is used to dynamically load a class from a module and inspect its attributes, methods,
    and other properties at runtime. This class supports checking the existence of classes, methods, properties,
    constants, and can also instantiate classes if they are not abstract.

    Attributes
    ----------
    classname : str, optional
        The name of the class to reflect upon.
    module_name : str, optional
        The name of the module where the class is defined.
    cls : type, optional
        The class object after it has been imported and assigned.
    """

    def __init__(self, classname: str = None, module: str = None):
        """
        Initializes the Reflection instance with optional class and module names.

        Parameters
        ----------
        classname : str, optional
            The name of the class to reflect upon.
        module : str, optional
            The name of the module where the class is defined.
        """
        self.classname = classname
        self.module_name = module
        self.cls = None
        if module:
            self.safeImport()

    def safeImport(self):
        """
        Safely imports the specified module and, if a classname is provided,
        assigns the class object to `self.cls`.

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

    def hasClass(self) -> bool:
        """
        Checks if the class exists within the module.

        Returns
        -------
        bool
            True if the class is defined, False otherwise.
        """
        return self.cls is not None

    def hasMethod(self, method_name: str) -> bool:
        """
        Checks if the class has a method with the specified name.

        Parameters
        ----------
        method_name : str
            The name of the method to check for.

        Returns
        -------
        bool
            True if the method exists, False otherwise.
        """
        return hasattr(self.cls, method_name)

    def hasProperty(self, prop: str) -> bool:
        """
        Checks if the class has a property with the specified name.

        Parameters
        ----------
        prop : str
            The name of the property to check for.

        Returns
        -------
        bool
            True if the property exists, False otherwise.
        """
        return hasattr(self.cls, prop)

    def hasConstant(self, constant: str) -> bool:
        """
        Checks if the class or module contains a constant with the specified name.

        Parameters
        ----------
        constant : str
            The name of the constant to check for.

        Returns
        -------
        bool
            True if the constant exists, False otherwise.
        """
        return hasattr(self.cls, constant)

    def getAttributes(self) -> list:
        """
        Retrieves all attributes of the class.

        Returns
        -------
        list
            A list of attribute names of the class.
        """
        return dir(self.cls) if self.cls else []

    def getConstructor(self):
        """
        Retrieves the constructor (__init__) of the class.

        Returns
        -------
        callable or None
            The constructor method if it exists, None otherwise.
        """
        return self.cls.__init__ if self.cls else None

    def getDocComment(self) -> str:
        """
        Retrieves the docstring of the class.

        Returns
        -------
        str or None
            The class docstring if available, None otherwise.
        """
        return self.cls.__doc__ if self.cls else None

    def getFileName(self) -> str:
        """
        Retrieves the file name where the class is defined.

        Returns
        -------
        str or None
            The file name if the class is found, None otherwise.
        """
        return inspect.getfile(self.cls) if self.cls else None

    def getMethod(self, method_name: str):
        """
        Retrieves the method with the specified name from the class.

        Parameters
        ----------
        method_name : str
            The name of the method to retrieve.

        Returns
        -------
        callable or None
            The method if found, None otherwise.
        """
        return getattr(self.cls, method_name, None) if self.cls else None

    def getMethods(self) -> list:
        """
        Retrieves all methods within the class.

        Returns
        -------
        list
            A list of method names in the class.
        """
        return inspect.getmembers(self.cls, predicate=inspect.isfunction) if self.cls else []

    def getName(self) -> str:
        """
        Retrieves the name of the class.

        Returns
        -------
        str or None
            The name of the class if available, None otherwise.
        """
        return self.cls.__name__ if self.cls else None

    def getParentClass(self):
        """
        Retrieves the parent class of the class.

        Returns
        -------
        tuple or None
            A tuple of base classes if available, None otherwise.
        """
        return self.cls.__bases__ if self.cls else None

    def getProperties(self) -> list:
        """
        Retrieves all properties within the class.

        Returns
        -------
        list
            A list of property names in the class.
        """
        return [prop for prop in dir(self.cls) if isinstance(getattr(self.cls, prop), property)] if self.cls else []

    def getProperty(self, prop: str):
        """
        Retrieves the value of a specified property.

        Parameters
        ----------
        prop : str
            The name of the property to retrieve.

        Returns
        -------
        any
            The value of the property if found, None otherwise.
        """
        return getattr(self.cls, prop, None) if self.cls else None

    def isAbstract(self) -> bool:
        """
        Checks if the class is abstract.

        Returns
        -------
        bool
            True if the class is abstract, False otherwise.
        """
        return hasattr(self.cls, '__abstractmethods__') and bool(self.cls.__abstractmethods__) if self.cls else False

    def isEnum(self) -> bool:
        """
        Checks if the class is an Enum.

        Returns
        -------
        bool
            True if the class is an Enum, False otherwise.
        """
        return isinstance(self.cls, type) and issubclass(self.cls, Enum) if self.cls else False

    def isIterable(self) -> bool:
        """
        Checks if the class is iterable.

        Returns
        -------
        bool
            True if the class is iterable, False otherwise.
        """
        return hasattr(self.cls, '__iter__') if self.cls else False

    def isInstantiable(self) -> bool:
        """
        Checks if the class can be instantiated (i.e., it is not abstract).

        Returns
        -------
        bool
            True if the class can be instantiated, False otherwise.
        """
        return self.cls is not None and callable(self.cls) and not self.is_abstract()

    def newInstance(self, *args, **kwargs):
        """
        Creates a new instance of the class with the provided arguments.

        Parameters
        ----------
        *args : tuple
            Arguments passed to the class constructor.
        **kwargs : dict
            Keyword arguments passed to the class constructor.

        Returns
        -------
        object
            A new instance of the class.

        Raises
        ------
        TypeError
            If the class cannot be instantiated.
        """
        if self.is_instantiable():
            return self.cls(*args, **kwargs)
        raise TypeError(f"Cannot instantiate class '{self.classname}'.")

    def __str__(self) -> str:
        """
        Returns a string representation of the Reflection instance.

        Returns
        -------
        str
            The string representation of the Reflection instance.
        """
        return f"<Reflection class '{self.classname}' in module '{self.module_name}'>"
