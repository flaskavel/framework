import argparse
from flaskavel.luminate.contracts.console.parser_interface import IParser

class Parser(IParser):
    """
    A class to handle dynamic parsing of command-line arguments using argparse.

    This class allows child classes to define their arguments and handle
    the parsing of arguments with error handling and custom messages.

    Attributes
    ----------
    argparse : argparse.ArgumentParser
        The argument parser instance used to register and parse arguments.
    args : list
        A list to store the parsed arguments.
    registered_arguments : set
        A set that keeps track of the registered argument names to avoid duplicates.
    """

    def __init__(self):
        """
        Initializes the Parser class with an instance of argparse.ArgumentParser.

        Sets up the parser with the description 'Flaskavel Argument Parser'
        and initializes the arguments store and registered argument tracker.
        """
        self.argparse = argparse.ArgumentParser(description='Flaskavel Argument Parser')

        # Store parsed arguments
        self.args = []

        # Track registered arguments to avoid duplicates
        self.registered_arguments = set()

    def setArguments(self, arguments: list):
        """
        Registers command-line arguments dynamically.

        This method registers each argument passed in the `arguments` list
        into the parser. Each entry in the list should be a tuple, where
        the first item is the argument name, and the second item is a dictionary
        of options to pass to `add_argument`.

        Parameters
        ----------
        arguments : list of tuple
            A list of tuples where each tuple contains the argument name
            (str) and a dictionary of options (such as 'type', 'required',
            'help', etc.).

        Notes
        -----
        If an argument is already registered, it will be skipped to avoid
        duplicate definitions.
        """
        for arg, options in arguments:
            if arg not in self.registered_arguments:
                self.argparse.add_argument(arg, **options)
                self.registered_arguments.add(arg)

    def argumentsParse(self, args):
        """
        Parses the provided command-line arguments.

        This method processes the arguments passed to it and stores them
        in `self.args`. If an error occurs during parsing, a helpful error
        message will be displayed.

        Parameters
        ----------
        args : list of str
            A list of command-line arguments to parse, typically `sys.argv`
            or custom input.

        Returns
        -------
        argparse.Namespace
            The parsed arguments as an object where each argument is an attribute.

        Raises
        ------
        ValueError
            If required arguments are missing or if there is an error
            during the parsing process.
        """
        try:
            self.args = self.argparse.parse_args(args)
            return self.args
        except argparse.ArgumentError as e:
            # Handle errors with argument parsing
            error_msg = f"Argument parsing error: {e}"
            self.argparse.error(error_msg)
        except SystemExit as e:
            # Handle SystemExit (which is raised by argparse) and re-raise it with a custom message
            error_msg = f"Argument parsing failed: {str(e)}"
            raise ValueError(f"{error_msg}. Please provide all required arguments: {', '.join(self.registered_arguments)}")

