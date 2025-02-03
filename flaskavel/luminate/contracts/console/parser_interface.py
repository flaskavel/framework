from abc import ABC, abstractmethod
from typing import List, Dict

class IParser(ABC):
    """
    Interface for dynamic command-line argument parsing.

    Defines methods required for registering, managing, and parsing
    command-line arguments.
    """

    @abstractmethod
    def setArguments(self, arguments: List[tuple]):
        """
        Registers command-line arguments dynamically.

        Parameters
        ----------
        arguments : list of tuple
            A list of tuples where each tuple contains:
            - str: The argument name (e.g., '--value')
            - dict: A dictionary of options (e.g., {'type': int, 'required': True})

        Notes
        -----
        If an argument is already registered, it is skipped to prevent duplication.
        """
        pass

    @abstractmethod
    def parseArgs(self, *args: str):
        """
        Adds positional arguments to the internal argument list.

        Parameters
        ----------
        *args : tuple of str
            Command-line arguments passed as positional arguments.

        Notes
        -----
        These arguments will be stored for later parsing.
        """
        pass

    @abstractmethod
    def parseKargs(self, **kargs: str):
        """
        Adds keyword arguments to the internal argument list.

        Parameters
        ----------
        **kargs : dict
            A dictionary where keys represent argument names and values are their assigned values.

        Notes
        -----
        This method formats keyword arguments as `--key="value"` and ensures values are safely quoted.
        """
        pass

    @abstractmethod
    def get(self):
        """
        Parses the collected command-line arguments.

        Returns
        -------
        argparse.Namespace
            The parsed arguments as an object where each argument is an attribute.

        Raises
        ------
        ValueError
            If required arguments are missing or an error occurs during parsing.
        """
        pass
