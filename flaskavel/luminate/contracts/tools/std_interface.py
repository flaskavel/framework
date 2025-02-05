from abc import ABC, abstractmethod

class IStdClass(ABC):
    """
    An abstract base class defining the contract for any StdClass-like object.
    This class ensures that any concrete implementation provides the necessary methods
    for attribute management and dynamic behavior.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        """
        Initializes the object with optional keyword arguments to set attributes.

        Parameters
        ----------
        kwargs : dict
            Key-value pairs to set as attributes.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        Returns
        -------
        str
            A formatted string showing the object's attributes.
        """
        pass

    @abstractmethod
    def toDict(self) -> dict:
        """
        Converts the object's attributes to a dictionary.

        Returns
        -------
        dict
            A dictionary representation of the object's attributes.
        """
        pass

    @abstractmethod
    def update(self, **kwargs) -> None:
        """
        Updates the object's attributes dynamically.

        Parameters
        ----------
        kwargs : dict
            Key-value pairs to update attributes.
        """
        pass
