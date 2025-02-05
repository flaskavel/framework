from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any
import argparse


class IParser(ABC):
    """
    Interface for a command-line argument parser.

    Defines the necessary methods for a command-line parser, ensuring
    consistency across implementations.
    """

    @abstractmethod
    def __init__(self, vars: Dict[str, Any], args: Tuple[Any, ...], kwargs: Dict[str, Any]):
        """
        Initializes the parser.

        Parameters
        ----------
        vars : dict
            A dictionary containing additional variables.
        args : tuple
            A tuple containing command-line arguments.
        kwargs : dict
            A dictionary containing keyword arguments.
        """
        pass

    @abstractmethod
    def setArguments(self, arguments: List[Tuple[str, Dict[str, Any]]]) -> None:
        """
        Registers command-line arguments dynamically.

        Parameters
        ----------
        arguments : list of tuple
            A list of tuples where each tuple contains:
            - str: The argument name (e.g., '--value')
            - dict: A dictionary of options (e.g., {'type': int, 'required': True})

        Raises
        ------
        ValueError
            If an argument is already registered.
        """
        pass

    @abstractmethod
    def recognize(self) -> None:
        """
        Processes and formats command-line arguments before parsing.

        Raises
        ------
        ValueError
            If an argument does not follow the correct format.
        """
        pass

    @abstractmethod
    def get(self) -> argparse.Namespace:
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
