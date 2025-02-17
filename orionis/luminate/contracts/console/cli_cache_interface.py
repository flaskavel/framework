from abc import ABC, abstractmethod
from orionis.luminate.cache.console.commands import CacheCommands

class ICLICache(ABC):
    """
    Interface for CLICache, defining the required methods for managing command caching.

    This interface enforces a contract for any class that implements caching functionality
    for command execution within the framework.
    """

    @abstractmethod
    def _load_commands(self) -> None:
        """
        Loads command modules from predefined directories.

        This method should traverse specified directories, locate Python files, and import them dynamically.
        Implementations should ensure that only relevant directories are processed.
        """
        pass

    @abstractmethod
    def getCommands(self) -> CacheCommands:
        """
        Returns the instance of CacheCommands containing the command cache.

        This method provides access to the CacheCommands instance, which holds the cached commands.

        Returns
        -------
        CacheCommands
            The instance of CacheCommands that holds the cached commands.
        """
        pass
