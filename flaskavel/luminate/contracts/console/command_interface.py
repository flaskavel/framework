from abc import ABC, abstractmethod

class ICommand(ABC):
    """
    Interface for managing and executing registered commands.

    This interface ensures that any class implementing it will provide a method
    for executing commands from a cache by their signature.
    """

    @abstractmethod
    def call(signature: str, **kwargs):
        """
        Calls a registered command from the CacheCommands singleton.

        This method retrieves the command class associated with the given
        signature, instantiates it, and executes the `handle` method of
        the command instance.

        Parameters
        ----------
        signature : str
            The unique identifier (signature) of the command to be executed.
        **kwargs : dict
            Additional keyword arguments to be passed to the command instance
            when it is created.

        Raises
        ------
        KeyError
            If no command with the given signature is found in the cache.
        RuntimeError
            If an error occurs while executing the command.
        """
        pass
