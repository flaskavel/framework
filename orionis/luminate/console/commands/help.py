from orionis.luminate.console.base.command import BaseCommand
from orionis.luminate.cache.console.commands import CacheCommands
from orionis.luminate.console.exceptions.cli_exception import CLIOrionisRuntimeError

class HelpCommand(BaseCommand):
    """
    Command class to display the list of available commands in the Orionis application.

    This command fetches all registered commands from the cache and presents them in a table format.
    """

    # Command signature used for execution.
    signature = "help"

    # Brief description of the command.
    description = "Prints the list of available commands along with their descriptions."

    def handle(self) -> None:
        """
        Execute the help command.

        This method retrieves all available commands from the cache, sorts them alphabetically,
        and displays them in a structured table format.

        Raises
        ------
        ValueError
            If an unexpected error occurs during execution, a ValueError is raised
            with the original exception message.
        """
        try:

            # Display the available commands
            self.newLine()
            self.textSuccessBold(" (CLI Interpreter) Available Commands: ")

            # Retrieve command cache
            cache = CacheCommands()

            # Fetch and store commands in a structured format
            rows = [[command, cache.get(command)['description']] for command in cache.commands]

            # Sort commands alphabetically
            rows_sorted = sorted(rows, key=lambda x: x[0])

            # Display the commands in a table format
            self.table(
                ["Signature", "Description"],
                rows_sorted
            )

            # Add a new line after the table
            self.newLine()

        except Exception as e:

            # Handle any unexpected error and display the error message
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e