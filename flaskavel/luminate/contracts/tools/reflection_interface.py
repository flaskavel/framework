from abc import ABC, abstractmethod
from typing import Any, List, Optional

class IReflection(ABC):
    """
    Interface for Reflection class to dynamically inspect and load classes and their attributes.
    This interface defines the contract for any class that performs reflection-based operations on Python classes.
    """

    @abstractmethod
    def hasClass(self) -> bool:
        """
        Checks if the class exists within the module.

        Returns
        -------
        bool
            True if the class is defined, False otherwise.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def getAttributes(self) -> List[str]:
        """
        Retrieves all attributes of the class.

        Returns
        -------
        list
            A list of attribute names of the class.
        """
        pass

    @abstractmethod
    def getConstructor(self) -> Optional[Any]:
        """
        Retrieves the constructor (__init__) of the class.

        Returns
        -------
        callable or None
            The constructor method if it exists, None otherwise.
        """
        pass

    @abstractmethod
    def getDocComment(self) -> Optional[str]:
        """
        Retrieves the docstring of the class.

        Returns
        -------
        str or None
            The class docstring if available, None otherwise.
        """
        pass

    @abstractmethod
    def getFileName(self) -> Optional[str]:
        """
        Retrieves the file name where the class is defined.

        Returns
        -------
        str or None
            The file name if the class is found, None otherwise.
        """
        pass

    @abstractmethod
    def getMethod(self, method_name: str) -> Optional[Any]:
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
        pass

    @abstractmethod
    def getMethods(self) -> List[str]:
        """
        Retrieves all methods within the class.

        Returns
        -------
        list
            A list of method names in the class.
        """
        pass

    @abstractmethod
    def getName(self) -> Optional[str]:
        """
        Retrieves the name of the class.

        Returns
        -------
        str or None
            The name of the class if available, None otherwise.
        """
        pass

    @abstractmethod
    def getParentClass(self) -> Optional[tuple]:
        """
        Retrieves the parent class of the class.

        Returns
        -------
        tuple or None
            A tuple of base classes if available, None otherwise.
        """
        pass

    @abstractmethod
    def getProperties(self) -> List[str]:
        """
        Retrieves all properties within the class.

        Returns
        -------
        list
            A list of property names in the class.
        """
        pass

    @abstractmethod
    def getProperty(self, prop: str) -> Optional[Any]:
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
        pass

    @abstractmethod
    def isAbstract(self) -> bool:
        """
        Checks if the class is abstract.

        Returns
        -------
        bool
            True if the class is abstract, False otherwise.
        """
        pass

    @abstractmethod
    def isEnum(self) -> bool:
        """
        Checks if the class is an Enum.

        Returns
        -------
        bool
            True if the class is an Enum, False otherwise.
        """
        pass

    @abstractmethod
    def isIterable(self) -> bool:
        """
        Checks if the class is iterable.

        Returns
        -------
        bool
            True if the class is iterable, False otherwise.
        """
        pass

    @abstractmethod
    def isInstantiable(self) -> bool:
        """
        Checks if the class can be instantiated.

        Returns
        -------
        bool
            True if the class can be instantiated, False otherwise.
        """
        pass

    @abstractmethod
    def newInstance(self, *args, **kwargs) -> Any:
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
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representation of the Reflection instance.

        Returns
        -------
        str
            The string representation of the Reflection instance.
        """
        pass
