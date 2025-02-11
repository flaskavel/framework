from abc import ABC, abstractmethod
from typing import Any

class ICLIRunner(ABC):
    """
    Interface for CLIRunner, defining the structure for handling CLI command execution.

    This interface ensures that any implementing class properly processes and executes CLI commands.

    Methods
    -------
    handle(signature: str = None, vars: dict = {}, *args, **kwargs) -> Any
        Processes and executes a CLI command based on provided arguments.
    """

    @abstractmethod
    def handle(self, signature: str = None, vars: dict = {}, *args, **kwargs) -> Any:
        """
        Processes and executes a CLI command.

        This method:
        - Determines whether the command is invoked from `sys.argv` or as a function.
        - Extracts the command signature and arguments.
        - Executes the command pipeline.
        - Logs execution status and handles errors.

        Parameters
        ----------
        signature : str, optional
            The command signature (default is None, meaning it is extracted from `sys.argv`).
        vars : dict, optional
            Named arguments for the command (default is an empty dictionary).
        *args
            Additional arguments for the command.
        **kwargs
            Additional keyword arguments for the command.

        Returns
        -------
        Any
            The output of the executed command.

        Raises
        ------
        ValueError
            If no command signature is provided.
        Exception
            If an unexpected error occurs during execution.
        """
        pass
