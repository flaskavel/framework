from orionis.framework import VERSION
from orionis.luminate.console.base.command import BaseCommand
from orionis.luminate.console.exceptions.cli_exception import CLIOrionisRuntimeError

class VersionCommand(BaseCommand):
    """
    Command class to display the current version of the Orionis framework.

    This command prints the version number of the framework in use.
    """

    # Command signature used for execution.
    signature = "version"

    # Brief description of the command.
    description = "Prints the version of the framework in use."

    def handle(self) -> None:
        """
        Execute the version command.

        This method retrieves and prints the version of the Orionis framework.

        Raises
        ------
        ValueError
            If an unexpected error occurs during execution, a ValueError is raised
            with the original exception message.
        """
        try:

            # Print the version number
            self.textSuccessBold(f"Orionis Framework v{VERSION}")

        except Exception as e:

            # Handle any unexpected error and display the error message
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e
