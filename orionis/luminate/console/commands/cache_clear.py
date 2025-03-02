import os
import shutil
from orionis.luminate.console.base.command import BaseCommand
from orionis.luminate.console.exceptions.cli_exception import CLIOrionisRuntimeError

class CacheClearCommand(BaseCommand):
    """
    Clears Python bytecode caches (__pycache__) within the project directory.

    This command recursively searches for and removes all `__pycache__` directories
    in the project folder to ensure that no stale bytecode files persist.

    Attributes
    ----------
    signature : str
        The unique identifier for the command, used to trigger its execution.
    description : str
        A brief summary describing the purpose of the command.
    """

    # The command signature used to execute this command.
    signature = 'cache:clear'

    # A brief description of the command.
    description = 'Clears the project cache by removing all __pycache__ directories.'

    def handle(self) -> None:
        """
        Executes the cache clearing process.

        This method performs the following actions:
        - Recursively searches the project directory for `__pycache__` directories.
        - Deletes all found `__pycache__` directories and their contents.
        - Logs a success message if the process completes successfully, or an error message if an exception occurs.
        """
        try:

            # Get the base project path
            base_path = os.getcwd()

            # Normalize the base path to ensure consistent formatting
            base_path = os.path.normpath(base_path)

            # Recursively traverse directories starting from the base path
            for root, dirs, files in os.walk(base_path, topdown=True):

                # Skip the 'venv' directory and its subdirectories
                if 'venv' in dirs:
                    dirs.remove('venv')

                # Check for __pycache__ directories
                if '__pycache__' in dirs:
                    pycache_path = os.path.join(root, '__pycache__')

                    # Attempt to remove the __pycache__ directory
                    try:
                        shutil.rmtree(pycache_path)
                    except OSError as e:
                        self.fail(f"Error removing {pycache_path}: {e}")

            # Log a success message once all caches are cleared
            self.success(message='The application cache has been successfully cleared.')

        except Exception as e:

            # Handle any unexpected error and display the error message
            raise CLIOrionisRuntimeError(f"An unexpected error occurred while clearing the cache: {e}") from e
