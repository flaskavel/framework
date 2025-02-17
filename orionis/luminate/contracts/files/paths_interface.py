from abc import ABC, abstractmethod

class ISkeletonPath(ABC):
    """
    Resolves the absolute path for a given relative directory based on the script's execution directory.
    Ensures that the requested path is a valid directory.

    Attributes
    ----------
    route : str
        The resolved absolute path to the directory.

    Methods
    -------
    __str__():
        Returns the absolute path as a string.
    """

    @abstractmethod
    def resolve(self) -> str:
        """
        Returns the absolute path as a string.

        Returns
        -------
        str
            The absolute directory path.
        """
        pass
