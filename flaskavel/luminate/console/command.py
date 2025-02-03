import time
from flaskavel.luminate.cache.console.commands import CacheCommands
from flaskavel.luminate.console.output.console import Console
from flaskavel.luminate.console.output.executor import Executor
from flaskavel.luminate.console.parser import Parser
from flaskavel.luminate.contracts.console.command_interface import ICommand

class Command(ICommand):
    """
    A class for managing and executing registered commands from the cache.

    This class allows calling a command from the CacheCommands singleton,
    passing the required signature and any necessary keyword arguments.
    """

    @staticmethod
    def call(signature: str, *args):
        """
        Calls a registered command from the CacheCommands singleton.

        This method retrieves the command class associated with the given
        signature, instantiates it, and then executes the `handle` method of
        the command instance.

        Parameters
        ----------
        signature : str
            The unique identifier (signature) of the command to be executed.
        *args : tuple
            Additional arguments to be passed to the command instance
            when it is created.

        Raises
        ------
        KeyError
            If no command with the given signature is found in the cache.
        RuntimeError
            If an error occurs while executing the command.
        """
        # Record the start time
        start_time = time.time()

        try:
            # Retrieve the command information from the CacheCommands singleton
            cache = CacheCommands()  # Access the singleton instance
            command_info = cache.get(signature)  # Get command data using the signature

            # Initialize the argument parser and set the arguments
            argParser = Parser()
            argParser.setArguments(command_info['arguments'])
            arguments = argParser.argumentsParse(args)

            # Print the start status to the console
            Executor.running(program=signature)

            # Retrieve the command class from the cached data
            command_class = command_info['class']

            # Instantiate the command class
            command_instance = command_class()

            # Execute the 'handle()' method with parsed arguments
            output = command_instance.handle(arguments)

            # Calculate the elapsed time for executing the command
            elapsed_time = round(time.time() - start_time, 2)

            # Indicate that the command has completed successfully
            Executor.done(program=signature, time=f"{elapsed_time}s")

            # Return the output of the command
            return output

        except KeyError as e:
            # Handle case when the command signature is not found in the cache
            Console.error(message=f"Command with signature '{signature}' not found in cache. Error: {e}")

        except Exception as e:
            # Handle unexpected errors during the command execution
            Console.error(message=f"An error occurred while executing the command '{signature}': {e}")

            # Calculate the elapsed time for executing the command (even in failure)
            elapsed_time = round(time.time() - start_time, 2)

            # Indicate that the command execution has failed
            Executor.fail(program=signature, time=f"{elapsed_time}s")

