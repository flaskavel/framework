from flaskavel.framework import VERSION
from flaskavel.luminate.console.register import register
from flaskavel.luminate.console.base.command import BaseCommand

@register.command
class VersionCommand(BaseCommand):
    """
    Command class to display the current version of the Flaskavel framework.

    This command prints the version number of the framework in use.
    """

    # Command signature used for execution.
    signature = "version"

    # Brief description of the command.
    description = "Prints the version of the framework in use."

    def handle(self) -> None:
        """
        Execute the version command.

        This method retrieves and prints the version of the Flaskavel framework.

        Raises
        ------
        ValueError
            If an unexpected error occurs during execution, a ValueError is raised
            with the original exception message.
        """
        try:

            # Print the version number
            self.textSuccessBold(f"Flaskavel Framework v{VERSION}")

        except Exception as e:

            # Raise a ValueError if an unexpected error occurs.
            raise ValueError(f"An unexpected error occurred: {e}") from e
