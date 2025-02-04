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

    Methods
    -------
    safe_import() :
        Safely imports the specified module and class.
    has_class() :
        Checks if the class is defined in the module.
    has_method(method_name) :
        Checks if the class has a method with the specified name.
    has_property(prop) :
        Checks if the class has a property with the specified name.
    has_constant(constant) :
        Checks if the class or module has a constant with the specified name.
    get_attributes() :
        Returns all attributes of the class.
    get_constructor() :
        Returns the class constructor (__init__).
    get_doc_comment() :
        Returns the class docstring.
    get_file_name() :
        Returns the file name where the class is defined.
    get_method(method_name) :
        Returns the method with the specified name.
    get_methods() :
        Returns all methods of the class.
    get_name() :
        Returns the class name.
    get_parent_class() :
        Returns the parent class of the class.
    get_properties() :
        Returns all properties of the class.
    get_property(prop) :
        Returns the value of the specified property.
    is_abstract() :
        Checks if the class is abstract.
    is_enum() :
        Checks if the class is an Enum.
    is_iterable() :
        Checks if the class is iterable.
    is_instantiable() :
        Checks if the class is instantiable.
    new_instance(*args, **kwargs) :
        Creates a new instance of the class with the provided arguments.
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
            self.safe_import()

    def safe_import(self):
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

    def has_class(self) -> bool:
        """
        Checks if the class exists within the module.

        Returns
        -------
        bool
            True if the class is defined, False otherwise.
        """
        return self.cls is not None

    def has_method(self, method_name: str) -> bool:
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

    def has_property(self, prop: str) -> bool:
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

    def has_constant(self, constant: str) -> bool:
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

    def get_attributes(self) -> list:
        """
        Retrieves all attributes of the class.

        Returns
        -------
        list
            A list of attribute names of the class.
        """
        return dir(self.cls) if self.cls else []

    def get_constructor(self):
        """
        Retrieves the constructor (__init__) of the class.

        Returns
        -------
        callable or None
            The constructor method if it exists, None otherwise.
        """
        return self.cls.__init__ if self.cls else None

    def get_doc_comment(self) -> str:
        """
        Retrieves the docstring of the class.

        Returns
        -------
        str or None
            The class docstring if available, None otherwise.
        """
        return self.cls.__doc__ if self.cls else None

    def get_file_name(self) -> str:
        """
        Retrieves the file name where the class is defined.

        Returns
        -------
        str or None
            The file name if the class is found, None otherwise.
        """
        return inspect.getfile(self.cls) if self.cls else None

    def get_method(self, method_name: str):
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

    def get_methods(self) -> list:
        """
        Retrieves all methods within the class.

        Returns
        -------
        list
            A list of method names in the class.
        """
        return inspect.getmembers(self.cls, predicate=inspect.isfunction) if self.cls else []

    def get_name(self) -> str:
        """
        Retrieves the name of the class.

        Returns
        -------
        str or None
            The name of the class if available, None otherwise.
        """
        return self.cls.__name__ if self.cls else None

    def get_parent_class(self):
        """
        Retrieves the parent class of the class.

        Returns
        -------
        tuple or None
            A tuple of base classes if available, None otherwise.
        """
        return self.cls.__bases__ if self.cls else None

    def get_properties(self) -> list:
        """
        Retrieves all properties within the class.

        Returns
        -------
        list
            A list of property names in the class.
        """
        return [prop for prop in dir(self.cls) if isinstance(getattr(self.cls, prop), property)] if self.cls else []

    def get_property(self, prop: str):
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

    def is_abstract(self) -> bool:
        """
        Checks if the class is abstract.

        Returns
        -------
        bool
            True if the class is abstract, False otherwise.
        """
        return hasattr(self.cls, '__abstractmethods__') and bool(self.cls.__abstractmethods__) if self.cls else False

    def is_enum(self) -> bool:
        """
        Checks if the class is an Enum.

        Returns
        -------
        bool
            True if the class is an Enum, False otherwise.
        """
        return isinstance(self.cls, type) and issubclass(self.cls, Enum) if self.cls else False

    def is_iterable(self) -> bool:
        """
        Checks if the class is iterable.

        Returns
        -------
        bool
            True if the class is iterable, False otherwise.
        """
        return hasattr(self.cls, '__iter__') if self.cls else False

    def is_instantiable(self) -> bool:
        """
        Checks if the class can be instantiated (i.e., it is not abstract).

        Returns
        -------
        bool
            True if the class can be instantiated, False otherwise.
        """
        return self.cls is not None and callable(self.cls) and not self.is_abstract()

    def new_instance(self, *args, **kwargs):
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
