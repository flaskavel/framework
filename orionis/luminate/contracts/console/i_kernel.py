from abc import ABC, abstractmethod
from typing import Any, Tuple

class ICLIKernel(ABC):
    """
    Interface for CLIKernel, defining the required method for handling CLI command execution.

    This interface ensures that any implementing class can process CLI arguments
    and delegate execution accordingly.

    Methods
    -------
    handle(*args: tuple[Any, ...]) -> Any
        Processes CLI arguments and delegates execution to the appropriate command runner.
    """

    @abstractmethod
    def handle(self, *args: Tuple[Any, ...]) -> Any:
        """
        Handles CLI command execution by forwarding arguments to a command runner.

        Parameters
        ----------
        *args : tuple[Any, ...]
            A tuple containing CLI arguments passed from the command line.

        Returns
        -------
        Any
            The result of the executed command.
        """
        pass
