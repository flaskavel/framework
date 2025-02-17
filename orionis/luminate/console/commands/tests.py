from orionis.luminate.facades.tests import UnitTests
from orionis.luminate.console.register import register
from orionis.luminate.console.base.command import BaseCommand

@register.command
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

            # Initialize the test suite using the custom testing framework.
            return UnitTests.execute()

        except Exception as e:

            # Raise a ValueError if an unexpected error occurs.
            raise ValueError(f"An unexpected error occurred: {e}") from e