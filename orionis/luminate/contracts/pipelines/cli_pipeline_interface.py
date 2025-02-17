from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class ICLIPipeline(ABC):
    """
    Interface for CLIPipeline, defining the structure for handling CLI command retrieval,
    argument parsing, and execution.

    Methods
    -------
    getCommand(signature: str) -> "ICLIPipeline"
        Retrieves a command from the cache based on its signature.

    parseArguments(vars: Optional[Dict[str, Any]] = None, *args, **kwargs) -> "ICLIPipeline"
        Parses command-line arguments using the framework's argument parser.

    execute() -> Any
        Executes the retrieved command using parsed arguments.
    """

    @abstractmethod
    def getCommand(self, signature: str) -> "ICLIPipeline":
        """
        Retrieves a command from the cache based on its signature.

        Parameters
        ----------
        signature : str
            The unique identifier of the command.

        Returns
        -------
        ICLIPipeline
            The current instance of the pipeline for method chaining.

        Raises
        ------
        ValueError
            If the command signature is not found in the cache.
        """
        pass

    @abstractmethod
    def parseArguments(self, vars: Optional[Dict[str, Any]] = None, *args, **kwargs) -> "ICLIPipeline":
        """
        Parses command-line arguments using the framework's argument parser.

        Parameters
        ----------
        vars : dict, optional
            A dictionary of predefined variables to be included in parsing.
        *args
            Positional arguments for the parser.
        **kwargs
            Keyword arguments for the parser.

        Returns
        -------
        ICLIPipeline
            The current instance of the pipeline for method chaining.

        Raises
        ------
        ValueError
            If an error occurs during argument parsing.
        """
        pass

    @abstractmethod
    def execute(self) -> Any:
        """
        Executes the retrieved command using parsed arguments.

        Returns
        -------
        Any
            The output of the command execution.

        Raises
        ------
        ValueError
            If the command instance is invalid.
        """
        pass
