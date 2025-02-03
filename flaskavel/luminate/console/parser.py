import argparse
import shlex
import types
from flaskavel.luminate.contracts.console.parser_interface import IParser

class Parser(IParser):
    """
    A command-line argument parser using argparse.

    This class provides methods for dynamically registering arguments,
    parsing positional and keyword arguments, and handling errors gracefully.

    Attributes
    ----------
    argparse : argparse.ArgumentParser
        The argument parser instance used for defining and parsing arguments.
    args : list
        A list storing the command-line arguments to be parsed.
    registered_arguments : set
        A set tracking registered argument names to prevent duplicates.
    """

    def __init__(self):
        """
        Initializes the Parser class.

        Creates an ArgumentParser instance with a predefined description.
        Also initializes storage for arguments and a set for registered arguments.
        """
        self.argparse = argparse.ArgumentParser(description='Flaskavel Argument Parser')

        # Store parsed arguments
        self.args = []

        # Track registered arguments to prevent duplicates
        self.registered_arguments = set()

    def setArguments(self, arguments: list):
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
        for arg, options in arguments:
            if arg not in self.registered_arguments:
                self.argparse.add_argument(arg, **options)
                self.registered_arguments.add(arg)

    def parseArgs(self, *args):
        """
        Adds positional arguments to the internal argument list.

        Parameters
        ----------
        args : tuple of str
            A tuple of command-line arguments passed as positional arguments.

        Notes
        -----
        These arguments will be stored for later parsing.
        """

        # Check if the arguments are passed as a single dictionary inside a tuple
        if (isinstance(args, tuple) and (len(args) == 1) and (isinstance(args[0], dict))):

            # Extract the dictionary of arguments
            all_args = args[0]

            # Get the first argument (typically script name or command identifier)
            first_arg:str = all_args.get(0)

            # Check if the first argument indicates a Python script or command alias (flaskavel or fk)
            if first_arg.endswith('.py') or first_arg in ['flaskavel', 'fk']:
                args = all_args[1:]

            else:

                # Keep the arguments as they are
                args = all_args

        # Process each argument passed in args
        for arg in args:

            # Strip leading/trailing spaces from the argument
            arg = arg.strip()

            # Validate that the argument starts with '--' and contains '=' in the expected format
            if arg.startswith('--') and '=' in arg[2:]:
                self.args.append(str(arg))
            else:
                raise ValueError(f'Unrecognized argument: "{str(arg)}". All command arguments must follow the convention: --key="value"')

    def parseKargs(self, **kargs):
        """
        Adds keyword arguments to the internal argument list.

        This method formats keyword arguments as `--key="value"` and ensures values are safely quoted.

        Parameters
        ----------
        **kargs : dict
            A dictionary where keys represent argument names and values are their assigned values.

        Notes
        -----
        If the argument value is a class, function, or lambda, a ValueError is raised.
        """
        for key, value in kargs.items():

            # Check if the value is an instance of a class
            if isinstance(value, type):
                raise ValueError("Command arguments cannot be instances of a class.")

            # Check if the value is a lambda or function
            elif (isinstance(value, types.LambdaType) or isinstance(value, types.FunctionType)):
                raise ValueError("Command arguments cannot be functions.")

            # Format the argument as '--key="value"' and append it to the args list
            else:
                self.args.append(f'--{key}={shlex.quote(str(value))}')

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
        try:
            parsed_args = self.argparse.parse_args(self.args)
            return vars(parsed_args)
        except argparse.ArgumentError as e:
            # Handle errors with argument parsing
            error_msg = f"Argument parsing error: {e}"
            self.argparse.error(error_msg)
        except SystemExit as e:
            # Handle SystemExit (which is raised by argparse) and re-raise it with a custom message
            error_msg = f"Argument parsing failed: {str(e)}"
            raise ValueError(f"{error_msg}. Please provide all required arguments: {', '.join(self.registered_arguments)}")
