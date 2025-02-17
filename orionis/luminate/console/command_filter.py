from orionis.luminate.contracts.console.command_filter_interface import ICommandFilter

# List of commands that should be excluded from output formatting
EXCLUDED_COMMANDS = [
    'schedule:work',   # Command to handle scheduled work
    'help',            # Command to show help information
    'version',         # Command to display version information
    'tests:run'        # Command to run tests
]

class CommandFilter(ICommandFilter):
    """
    CommandFilter handles the exclusion of specific commands from output formatting.

    This class:
    - Determines whether a command should be excluded from output formatting based on a predefined list.
    - Can be extended or modified to support more advanced filtering if needed.

    Methods
    -------
    isExcluded(command: str) -> bool
        Checks if the given command is excluded from output formatting.
    """

    @staticmethod
    def isExcluded(command: str) -> bool:
        """
        Checks if the given command is in the excluded commands list.

        Parameters
        ----------
        command : str
            The command to check.

        Returns
        -------
        bool
            Returns True if the command is excluded from output formatting, False otherwise.
        """
        return command in EXCLUDED_COMMANDS
