from abc import ABC, abstractmethod
from typing import Any, Callable

class ICacheCommands(ABC):
    """
    CacheCommands is a class that manages the registration, unregistration, and retrieval of command instances.

    Methods
    -------
    __init__()
        Initializes the command cache with an empty dictionary.
    register(signature: str, description: str, arguments: list, concrete: Callable[..., Any])
        Register a new command with its signature, description, and class instance.
    unregister(signature: str)
        Unregister an existing command by its signature.
    get(signature: str)
        Retrieve the information of a registered command by its signature.
    """

    @abstractmethod
    def register(self, signature: str, description: str, arguments: list, concrete: Callable[..., Any]):
        """
        Register a new command with its signature, description, and class instance.

        Parameters
        ----------
        signature : str
            The unique identifier (signature) for the command.
        description : str
            A brief description of what the command does.
        concrete : class
            The class or callable instance that defines the command behavior.

        Raises
        ------
        ValueError
            If a command with the given signature already exists.
        """
        pass

    @abstractmethod
    def unregister(self, signature: str):
        """
        Unregister an existing command by its signature.

        Parameters
        ----------
        signature : str
            The unique identifier (signature) for the command to unregister.

        Raises
        ------
        KeyError
            If the command with the given signature does not exist.
        """
        pass

    @abstractmethod
    def get(self, signature: str):
        """
        Retrieve the information of a registered command by its signature.

        Parameters
        ----------
        signature : str
            The unique identifier (signature) for the command.

        Returns
        -------
        dict
            A dictionary containing the class, signature, and description of the command.

        Raises
        ------
        KeyError
            If the command with the given signature does not exist.
        """
        pass
