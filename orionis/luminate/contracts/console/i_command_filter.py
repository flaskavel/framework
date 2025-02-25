from abc import ABC, abstractmethod

class ICommandFilter(ABC):
    """
    CommandFilter handles the exclusion of specific commands from output formatting.

    This class:
    - Determines whether a command should be excluded from output formatting based on a predefined list.
    - Can be extended or modified to support more advanced filtering if needed.

    Methods
    -------
    isExcluded(command: str) -> bool
        Checks if the given command is excluded from output formatting.
    """

    @abstractmethod
    def isExcluded(command: str) -> bool:
        """
        Checks if the given command is in the excluded commands list.

        Parameters
        ----------
        command : str
            The command to check.

        Returns
        -------
        bool
            Returns True if the command is excluded from output formatting, False otherwise.
        """
        pass
