import shlex
import types
import argparse
from io import StringIO
from contextlib import redirect_stderr
from orionis.luminate.contracts.console.parser_interface import IParser

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
    kwargs : dict
        A dictionary containing keyword arguments.
    registered_arguments : set
        A set tracking registered argument names to prevent duplicates.
    """

    def __init__(self, vars: dict, args: tuple, kwargs: dict):
        """
        Initializes the Parser class.

        Parameters
        ----------
        vars : dict
            A dictionary containing additional variables.
        args : tuple
            A tuple containing command-line arguments.
        kwargs : dict
            A dictionary containing keyword arguments.
        """
        self.argparse = argparse.ArgumentParser(description='Orionis Commands Argument Parser')
        self.vars = vars or {}
        self.args = list(args)
        self.kwargs = kwargs or {}
        self.registered_arguments = set()
        self.parsed_arguments = []

    def setArguments(self, arguments: list):
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
        for arg, options in arguments:
            if arg in self.registered_arguments:
                raise ValueError(f"Duplicate argument detected: {arg}")
            self.argparse.add_argument(arg, **options)
            self.registered_arguments.add(arg)

    def _validateType(self, value):
        """
        Validates that a value is not an instance of a class, function, or lambda.

        Parameters
        ----------
        value : any
            The value to be validated.

        Raises
        ------
        ValueError
            If the value is a class instance, function, or lambda.
        """
        if isinstance(value, (types.FunctionType, types.LambdaType, type)):
            raise ValueError("Command arguments cannot be functions, lambdas, or class instances.")

    def recognize(self):
        """
        Processes and formats command-line arguments before parsing.

        Raises
        ------
        ValueError
            If an argument does not follow the correct format.
        """

        # If `args` is a single list inside a list, extract it
        if isinstance(self.args, list) and len(self.args) == 1 and isinstance(self.args[0], list):
            all_args:list = self.args[0]
            first_arg:str = all_args[0]

            if first_arg.endswith('.py') or first_arg in ['orionis']:
                self.args = all_args[1:]
            else:
                self.args = all_args

        # Merge `kwargs` with `vars`
        if isinstance(self.vars, dict):
            self.kwargs = {**self.vars, **self.kwargs}
        else:
            self.args = [self.vars, *self.args]

        # Process each argument in `args`
        formatted_args = []
        for arg in self.args:
            self._validateType(arg)

            arg = str(arg).strip()
            if arg.startswith('--') and '=' in arg[2:]:
                formatted_args.append(arg)
            else:
                raise ValueError(f'Unrecognized argument: "{arg}". Expected format: --key="value"')

        # Convert `kwargs` to `--key=value` format
        for key, value in self.kwargs.items():
            self._validateType(value)
            formatted_args.append(f'--{key}={shlex.quote(str(value))}')

        # Replace args with processed version
        self.parsed_arguments = formatted_args

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
            If required arguments are missing or an error occurs during parsing,
            it raises a customized error message including the original argparse error.
        """
        stderr_capture = StringIO()

        try:
            with redirect_stderr(stderr_capture):
                return self.argparse.parse_args(self.parsed_arguments)

        except SystemExit:
            error_message = stderr_capture.getvalue().strip()
            array_message = error_message.split('error: ')
            final_message = str(array_message[1]).replace('unrecognized', 'Unrecognized')
            raise ValueError(f"Argument parsing failed | {final_message} | Required arguments: {', '.join(self.registered_arguments)}")

        except Exception as e:
            raise ValueError(f"An unexpected error occurred while parsing arguments: {str(e)}")
