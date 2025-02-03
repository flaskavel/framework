from abc import ABC, abstractmethod

class IParser(ABC):
    """
    Interface for dynamic command-line argument parsing with argparse.

    This interface defines the methods required for handling argument registration
    and parsing, ensuring that any concrete implementation adheres to the expected
    behavior.
    """

    @abstractmethod
    def setArguments(self, arguments: list):
        """
        Registers the command-line arguments.

        Parameters
        ----------
        arguments : list of tuple
            A list of tuples where each tuple contains the argument name (str)
            and a dictionary of options (such as 'type', 'required', 'help', etc.).
        """
        pass

    @abstractmethod
    def argumentsParse(self, args: list):
        """
        Parses the provided command-line arguments.

        Parameters
        ----------
        args : list of str
            A list of command-line arguments to parse.

        Returns
        -------
        argparse.Namespace
            The parsed arguments as an object where each argument is an attribute.

        Raises
        ------
        ValueError
            If required arguments are missing or if there is an error during 
            the parsing process.
        """
        pass
