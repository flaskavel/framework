from orionis.luminate.console.exceptions.cli_exception import CLIOrionisRuntimeError
from orionis.luminate.console.base.command import BaseCommand
from orionis.luminate.facades.tests.tests_facade import UnitTests

class TestsCommand(BaseCommand):
    """
    Command class to display the list of available commands in the Orionis application.

    This command fetches all registered commands from the cache and presents them in a table format.
    """

    # Command signature used for execution.
    signature = "tests:run"

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
            return UnitTests.execute()
        except Exception as e:
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e