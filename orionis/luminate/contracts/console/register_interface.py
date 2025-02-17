from abc import ABC, abstractmethod

class IRegister(ABC):
    """
    Interface for a command register.
    """

    @abstractmethod
    def command(self, command_class):
        """
        Registers a command class after validating its structure.

        Parameters
        ----------
        command_class : type
            The command class to register.

        Returns
        -------
        type
            The registered command class.

        Raises
        ------
        ValueError
            If 'signature' is missing, invalid, contains spaces, or is not a string.
            If 'description' is missing or not a string.
            If 'handle' method is missing.
        TypeError
            If the class does not inherit from 'BaseCommand'.
        """
        pass