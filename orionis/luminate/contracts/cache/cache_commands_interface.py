from abc import ABC, abstractmethod

class ICacheCommands(ABC):
    """
    Interface for managing a cache of commands.

    This interface ensures that any class implementing it will provide methods
    for registering, unregistering, and retrieving commands.
    """

    @abstractmethod
    def register(self, signature: str, description: str, instance):
        """
        Register a new command with its signature, description, and class instance.

        Parameters
        ----------
        signature : str
            The unique identifier (signature) for the command.
        description : str
            A brief description of what the command does.
        instance : class
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
