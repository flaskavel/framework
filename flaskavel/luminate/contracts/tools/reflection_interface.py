from abc import ABC, abstractmethod
from typing import Any, List, Optional

class IReflection(ABC):
    """
    Abstract base class for reflection operations on a Python class.
    This interface defines the methods that any reflection class must implement.
    """

    @abstractmethod
    def safeImport(self):
        """
        Safely imports the module and class as specified in the instance.
        """
        pass

    @abstractmethod
    def getFile(self) -> str:
        """
        Retrieves the file path where the class is defined.

        Returns
        -------
        str
            The file path of the class definition.
        """
        pass

    @abstractmethod
    def hasClass(self) -> bool:
        """
        Checks whether the class object is available.

        Returns
        -------
        bool
            True if the class is loaded, False otherwise.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def getAttributes(self) -> List[str]:
        """
        Retrieves a list of all attributes (including methods and properties) of the class.

        Returns
        -------
        list
            A list of attribute names in the class.
        """
        pass

    @abstractmethod
    def getConstructor(self):
        """
        Retrieves the constructor (__init__) of the class.

        Returns
        -------
        function or None
            The constructor method if available, otherwise None.
        """
        pass

    @abstractmethod
    def getDocComment(self) -> Optional[str]:
        """
        Retrieves the docstring of the class.

        Returns
        -------
        str or None
            The docstring of the class if available, otherwise None.
        """
        pass

    @abstractmethod
    def getFileName(self, remove_extension: bool = False) -> str:
        """
        Retrieves the file name where the class is defined.

        Parameters
        ----------
        remove_extension : bool, optional
            If True, the file extension will be removed from the filename. Default is False.

        Returns
        -------
        str
            The file name of the class definition.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def getMethods(self) -> List[str]:
        """
        Retrieves a list of all methods in the class.

        Returns
        -------
        list
            A list of method names in the class.
        """
        pass

    @abstractmethod
    def getName(self) -> str:
        """
        Retrieves the name of the class.

        Returns
        -------
        str or None
            The name of the class if available, otherwise None.
        """
        pass

    @abstractmethod
    def getParentClass(self) -> Optional[tuple]:
        """
        Retrieves the parent classes (base classes) of the class.

        Returns
        -------
        tuple or None
            A tuple of base classes if available, otherwise None.
        """
        pass

    @abstractmethod
    def getProperties(self) -> List[str]:
        """
        Retrieves a list of all properties of the class.

        Returns
        -------
        list
            A list of property names in the class.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def isAbstract(self) -> bool:
        """
        Checks whether the class is abstract.

        Returns
        -------
        bool
            True if the class is abstract, False otherwise.
        """
        pass

    @abstractmethod
    def isEnum(self) -> bool:
        """
        Checks whether the class is an enumeration.

        Returns
        -------
        bool
            True if the class is a subclass of Enum, False otherwise.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def isIterable(self) -> bool:
        """
        Checks whether the class is iterable.

        Returns
        -------
        bool
            True if the class is iterable, False otherwise.
        """
        pass

    @abstractmethod
    def isInstantiable(self) -> bool:
        """
        Checks whether the class can be instantiated.

        Returns
        -------
        bool
            True if the class is callable and not abstract, False otherwise.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representation of the Reflection instance.

        Returns
        -------
        str
            A string describing the class and module.
        """
        pass
