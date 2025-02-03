from flaskavel.luminate.cache.console.commands import CacheCommands
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
        try:
            # Retrieve the command information from the CacheCommands singleton
            cache = CacheCommands()  # Access the singleton instance
            command_info = cache.get(signature)  # Get command data using the signature

            # Retrieve the command class from the cached data
            command_class = command_info['class']

            # Instantiate the command class with the provided keyword arguments
            command_instance = command_class(**kwargs)

            # Execute the handle() method of the command instance
            command_instance.handle()

        except KeyError as e:
            raise KeyError(f"Command with signature '{signature}' not found.") from e
        except Exception as e:
            raise RuntimeError(f"Error executing the command '{signature}': {e}") from e
