import argparse
from typing import Dict, Any, Optional
from flaskavel.luminate.console.parser import Parser
from flaskavel.luminate.console.cache import CLICache
from flaskavel.luminate.console.base.command import BaseCommand
from flaskavel.luminate.contracts.pipelines.cli_pipeline_interface import ICLIPipeline

class CLIPipeline(ICLIPipeline):
    """
    Handles the retrieval, parsing, and execution of CLI commands within the Flaskavel framework.

    This class is responsible for:
    - Retrieving command metadata from cache.
    - Parsing command-line arguments dynamically.
    - Executing the corresponding command with parsed arguments.

    Attributes
    ----------
    _command : dict
        Stores the command's metadata, including its instance and expected arguments.
    _parsed_arguments : argparse.Namespace
        Holds parsed arguments after processing user input.
    """

    def __init__(self):
        """
        Initializes the CLIPipeline instance with an empty command cache
        and a default argument namespace.
        """
        self._command: Dict[str, Any] = {}
        self._parsed_arguments: argparse.Namespace = argparse.Namespace()

    def getCommand(self, signature: str) -> "CLIPipeline":
        """
        Retrieves a command from the cache based on its signature.

        Parameters
        ----------
        signature : str
            The unique identifier of the command.

        Returns
        -------
        CLIPipeline
            The current instance of CLIPipeline for method chaining.

        Raises
        ------
        ValueError
            If the command signature is not found in the cache.
        """
        try:
            cache = CLICache().getCommands()
            self._command = cache.get(signature)
            return self
        except KeyError as e:
            raise ValueError(e)

    def parseArguments(self, vars: Optional[Dict[str, Any]] = None, *args, **kwargs) -> "CLIPipeline":
        """
        Parses command-line arguments using the Flaskavel argument parser.

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
        CLIPipeline
            The current instance of CLIPipeline for method chaining.

        Raises
        ------
        ValueError
            If an error occurs during argument parsing.
        """
        try:
            arguments = self._command.get("arguments")
            if arguments:
                arg_parser = Parser(vars=vars or {}, args=args, kwargs=kwargs)
                arg_parser.setArguments(arguments=arguments)
                arg_parser.recognize()
                self._parsed_arguments = arg_parser.get()

            return self

        except Exception as e:
            raise ValueError(f"Error parsing arguments: {e}")

    def execute(self) -> Any:
        """
        Executes the retrieved command using parsed arguments.

        This method:
        - Instantiates the command class.
        - Calls the `handle()` method, passing the parsed arguments.

        Returns
        -------
        Any
            The output of the command execution.

        Raises
        ------
        ValueError
            If the command instance is invalid.
        """
        command_class = self._command.get("instance")
        command_instance: BaseCommand = command_class()
        command_instance.setArgs(self._parsed_arguments)
        return command_instance.handle(**vars(self._parsed_arguments))
