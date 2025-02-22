from abc import ABC, abstractmethod

class IStdClass(ABC):
    """
    Interface for a dynamic class that allows setting arbitrary attributes,
    similar to PHP's stdClass.
    """

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
    def update(self, **kwargs):
        """
        Updates the object's attributes dynamically.

        Parameters
        ----------
        kwargs : dict
            Key-value pairs to update attributes.
        """
        pass
