import time
from flaskavel.luminate.cache.console.commands import CacheCommands
from flaskavel.luminate.console.output.console import Console
from flaskavel.luminate.console.output.executor import Executor
from flaskavel.luminate.contracts.console.command_interface import ICommand

class Command(ICommand):
    """
    A class for managing and executing registered commands from the cache.

    This class allows calling a command from the CacheCommands singleton,
    passing the required signature and any necessary keyword arguments.
    """

    @staticmethod
    def call(signature: str, **kwargs):
        """
        Calls a registered command from the CacheCommands singleton.

        This method retrieves the command class associated with the given
        signature, instantiates it, and then executes the `handle` method of
        the command instance.

        Parameters
        ----------
        signature : str
            The unique identifier (signature) of the command to be executed.
        **kwargs : dict
            Additional keyword arguments to be passed to the command instance
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

            # Print Executor Console
            Executor.running(program=signature)

            # Retrieve the command class from the cached data
            command_class = command_info['class']

            # Instantiate the command class
            command_instance = command_class()

            # Execute the handle() method of the command instance with the provided keyword arguments
            output = command_instance.handle(**kwargs)

            # Calculate the time taken to execute the command
            elapsed_time = round(time.time() - start_time, 2)

            # Indicate that the command has completed successfully
            Executor.done(program=signature, time=f"{elapsed_time}s")

            # Return Outpout Command
            return output

        except KeyError as e:

            # Handle case when the command signature is not found in the cache
            Console.error(message=e)

        except Exception as e:

            # Handle other exceptions during the execution of the command
            Console.error(message=e)

            # Calculate the time taken to execute the command
            elapsed_time = round(time.time() - start_time, 2)

             # Indicate that the command has failed
            Executor.fail(program=signature, time=f"{elapsed_time}s")
