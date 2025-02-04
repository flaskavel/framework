from typing import Any, Callable, List, Optional


class IReflection:
    """
    A class that allows for reflection on a Python class and its components.
    It provides functionality to inspect modules, classes, methods, properties,
    and constants dynamically.

    Attributes
    ----------
    classname : str, optional
        The name of the class to reflect on. (Default is None)
    module_name : str, optional
        The name of the module where the class is located. (Default is None)
    cls : type, optional
        The class object itself after successful import.

    Methods
    -------
    safe_import() -> None
        Attempts to import the module and class safely. Raises ValueError if import fails.
    has_class() -> bool
        Checks if the class exists in the module.
    has_method(method_name: str) -> bool
        Checks if the class has the specified method.
    has_property(prop: str) -> bool
        Checks if the class has the specified property.
    has_constant(constant: str) -> bool
        Checks if the class/module has the specified constant.
    get_attributes() -> List[str]
        Returns a list of all attributes of the class.
    get_constructor() -> Optional[Callable]
        Returns the class constructor (__init__) or None if not available.
    get_doc_comment() -> Optional[str]
        Returns the docstring for the class or None if not available.
    get_file_name() -> Optional[str]
        Returns the file path where the class is defined.
    get_method(method_name: str) -> Optional[Callable]
        Returns the specified method or None if not found.
    get_methods() -> List[Callable]
        Returns a list of all methods of the class.
    get_name() -> Optional[str]
        Returns the full name of the class.
    get_parent_class() -> Optional[tuple]
        Returns the parent classes of the class, or None if no parent exists.
    get_properties() -> List[str]
        Returns a list of all properties of the class.
    get_property(prop: str) -> Optional[Any]
        Returns the value of a specified property or None if not found.
    is_abstract() -> bool
        Checks if the class is abstract.
    is_enum() -> bool
        Checks if the class is an Enum.
    is_iterable() -> bool
        Checks if the class is iterable.
    is_instantiable() -> bool
        Checks if the class can be instantiated.
    new_instance(*args, **kwargs) -> Any
        Creates a new instance of the class with the given arguments.
    __str__() -> str
        Returns a string representation of the Reflection object.
    """

    def __init__(self, classname: Optional[str] = None, module: Optional[str] = None):
        """
        Initializes the Reflection instance with an optional class name and module.

        Parameters
        ----------
        classname : str, optional
            The name of the class to reflect on. (Default is None)
        module : str, optional
            The name of the module where the class is located. (Default is None)
        """

        pass

    def safe_import(self) -> None:
        """
        Safely imports the class from the specified module.

        Raises
        ------
        ValueError
            If the class cannot be found in the module or if the import fails.
        """
        pass

    def has_class(self) -> bool:
        """
        Checks if the class exists in the specified module.

        Returns
        -------
        bool
            True if the class exists, False otherwise.
        """
        pass

    def has_method(self, method_name: str) -> bool:
        """
        Checks if the class has a specified method.

        Parameters
        ----------
        method_name : str
            The name of the method to check.

        Returns
        -------
        bool
            True if the method exists in the class, False otherwise.
        """
        pass

    def has_property(self, prop: str) -> bool:
        """
        Checks if the class has a specified property.

        Parameters
        ----------
        prop : str
            The name of the property to check.

        Returns
        -------
        bool
            True if the property exists, False otherwise.
        """
        pass

    def has_constant(self, constant: str) -> bool:
        """
        Checks if the class or module has the specified constant.

        Parameters
        ----------
        constant : str
            The name of the constant to check.

        Returns
        -------
        bool
            True if the constant exists, False otherwise.
        """
        pass

    def get_attributes(self) -> List[str]:
        """
        Returns a list of all attributes of the class.

        Returns
        -------
        list of str
            A list of attribute names in the class.
        """
        pass

    def get_constructor(self) -> Optional[Callable]:
        """
        Returns the constructor (__init__) of the class, or None if not available.

        Returns
        -------
        Callable or None
            The constructor of the class or None if it doesn't exist.
        """
        pass

    def get_doc_comment(self) -> Optional[str]:
        """
        Returns the class's docstring.

        Returns
        -------
        str or None
            The docstring of the class or None if not available.
        """
        pass

    def get_file_name(self) -> Optional[str]:
        """
        Returns the file path where the class is defined.

        Returns
        -------
        str or None
            The file path of the class or None if not available.
        """
        pass

    def get_method(self, method_name: str) -> Optional[Callable]:
        """
        Returns the specified method of the class by name.

        Parameters
        ----------
        method_name : str
            The name of the method to retrieve.

        Returns
        -------
        Callable or None
            The method if found, or None if not found.
        """
        pass

    def get_methods(self) -> List[Callable]:
        """
        Returns a list of all methods of the class.

        Returns
        -------
        list of Callable
            A list of methods of the class.
        """
        pass

    def get_name(self) -> Optional[str]:
        """
        Returns the full name of the class.

        Returns
        -------
        str or None
            The name of the class or None if not available.
        """
        pass

    def get_parent_class(self) -> Optional[tuple]:
        """
        Returns the parent classes of the class, or None if no parent exists.

        Returns
        -------
        tuple or None
            A tuple of parent classes or None if there is no parent class.
        """
        pass

    def get_properties(self) -> List[str]:
        """
        Returns a list of all properties of the class.

        Returns
        -------
        list of str
            A list of properties of the class.
        """
        pass

    def get_property(self, prop: str) -> Optional[Any]:
        """
        Returns the value of a specified property.

        Parameters
        ----------
        prop : str
            The name of the property to retrieve.

        Returns
        -------
        Any or None
            The value of the property or None if not found.
        """
        pass

    def is_abstract(self) -> bool:
        """
        Checks if the class is abstract.

        Returns
        -------
        bool
            True if the class is abstract, False otherwise.
        """
        pass

    def is_enum(self) -> bool:
        """
        Checks if the class is an Enum.

        Returns
        -------
        bool
            True if the class is an Enum, False otherwise.
        """
        pass

    def is_iterable(self) -> bool:
        """
        Checks if the class is iterable.

        Returns
        -------
        bool
            True if the class is iterable, False otherwise.
        """
        pass

    def is_instantiable(self) -> bool:
        """
        Checks if the class is instantiable.

        Returns
        -------
        bool
            True if the class is instantiable, False otherwise.
        """
        pass

    def new_instance(self, *args, **kwargs) -> Any:
        """
        Creates a new instance of the class with the given arguments.

        Parameters
        ----------
        *args : tuple
            Arguments to pass to the constructor.
        **kwargs : dict
            Keyword arguments to pass to the constructor.

        Returns
        -------
        Any
            A new instance of the class.

        Raises
        ------
        TypeError
            If the class is not instantiable.
        """
        pass

    def __str__(self) -> str:
        """
        Returns a string representation of the class details.

        Returns
        -------
        str
            A string describing the class.
        """
        pass
