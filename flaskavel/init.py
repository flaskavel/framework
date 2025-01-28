import os
import re
import sys
import shutil
import tempfile
import argparse
import subprocess
from unicodedata import normalize
from flaskavel.metadata import SKELETON, NAME, DOCS
from flaskavel.lab.beaker.console.output import Console

# Definition of the _Display class
class _Display:
    """
    Class for specific use within this file.
    Provides static methods to display messages to the console,
    such as welcome messages, informational messages, failure messages, and error messages.
    """

    # Static method to display a welcome message
    @staticmethod
    def welcome():
        """
        Displays a welcome message to the framework.
        This method does not take any parameters and does not return any value.
        """
        # Calls Console.newLine() to add a new line in the console
        Console.newLine()
        # Displays a success message using Console.textSuccess()
        Console.textSuccess(message=f"Thank you for using {NAME}, welcome.")

    # Static method to display an informational message
    @staticmethod
    def info(message: str = ''):
        """
        Displays an informational message to the console.

        Parameters:
            message (str): The message to display. Defaults to an empty string.
        """
        # Formats the message with a specific prefix
        output = f"[Flaskavel Init Project] - {message}"
        # Calls Console.info() to display the message with a timestamp
        Console.info(message=output, timestamp=True)

    # Static method to display a failure message
    @staticmethod
    def fail(message: str = ''):
        """
        Displays a failure message to the console.

        Parameters:
            message (str): The message to display. Defaults to an empty string.
        """
        # Formats the message with a specific prefix
        output = f"[Flaskavel Init Project] - {message}"
        # Calls Console.fail() to display the message with a timestamp
        Console.fail(message=output, timestamp=True)

    # Static method to display an error message and terminate the program
    @staticmethod
    def error(message: str = ''):
        """
        Displays an error message to the console and terminates the program.

        Parameters:
            message (str): The message to display. Defaults to an empty string.
        """
        # Formats the message with a specific prefix
        output = f"[Flaskavel Init Project] - {message}"
        # Calls Console.error() to display the message with a timestamp
        Console.error(message=output, timestamp=True)
        # Adds a new line in the console
        Console.newLine()
        # Terminates the program with an exit code of 1 (indicating an error)
        sys.exit(1)

class _FlaskavelInit:

    def __init__(self, name_app:str=None):
        """
        Convert the name to lowercase, replace spaces with underscores, and strip surrounding whitespace
        """
        self.name_app_folder = self._sanitize_folder_name(name_app or f"{NAME}_app")

    def _sanitize_folder_name(self, name: str) -> str:
        """
        Sanitize a folder name to ensure it is valid across different operating systems.

        Steps:
        1. Normalize text to remove accents and special characters.
        2. Convert to lowercase.
        3. Replace spaces with underscores.
        4. Remove invalid characters (e.g., \ / : * ? " < > |).
        5. Strip leading and trailing whitespace.
        6. Enforce length limit (255 characters).
        7. Ensure the result contains only valid characters.

        Args:
            name (str): The original folder name.

        Returns:
            str: A sanitized and valid folder name.

        Raises:
            ValueError: If the resulting name is empty or contains invalid characters.
        """
        if not name:
            raise ValueError("Folder name cannot be empty.")

        # Normalize to remove accents and special characters
        name = normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")

        # Convert to lowercase
        name = name.lower()

        # Replace spaces with underscores
        name = name.replace(" ", "_")

        # Remove invalid characters for folder names
        name = re.sub(r'[\\/:*?"<>|]', '', name)

        # Strip leading and trailing whitespace
        name = name.strip()

        # Limit the length to 255 characters
        name = name[:255]

        # Validate against allowed characters
        if not re.match(r'^[a-z0-9_-]+$', name):
            raise ValueError("The folder name can only contain letters, numbers, underscores, and hyphens.")

        if not name:
            raise ValueError("The sanitized folder name is empty after processing.")

        return name

    def handle(self):

        try:

            # Clone the repository
            _Display.info(f"Cloning the repository into '{self.name_app_folder}'... (Getting Latest Version)")
            subprocess.run(["git", "clone", SKELETON, self.name_app_folder], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _Display.info(f"Repository successfully cloned into '{self.name_app_folder}'.",)

            # Change to the project directory
            project_path = os.path.join(os.getcwd(), self.name_app_folder)
            os.chdir(project_path)
            _Display.info(f"Entering directory '{self.name_app_folder}'.")

            # Create a virtual environment
            _Display.info("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _Display.info("Virtual environment successfully created.")

            # Virtual environment path
            venv_path = os.path.join(project_path, "venv", "Scripts" if os.name == "nt" else "bin")

            # Check if requirements.txt exists
            if not os.path.exists("requirements.txt"):
                raise ValueError(f"'requirements.txt' not found. Please visit the Flaskavel Docs for more details: {DOCS}")

            else:

                # Install dependencies from requirements.txt
                _Display.info("Installing dependencies from 'requirements.txt'...")
                subprocess.run([os.path.join(venv_path, "pip"), "install", "-r", "requirements.txt"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                _Display.info("Dependencies successfully installed.")

                # Create .env
                example_env_path = os.path.join(project_path,'.env.example')
                env_path = os.path.join(project_path,'.env')
                shutil.copy(example_env_path, env_path)

                # Create ApiKey
                os.chdir(project_path)
                subprocess.run([sys.executable, '-B', 'reactor', 'key:generate'], capture_output=True, text=True)

                # remove .git origin
                subprocess.run(["git", "remote", "remove", "origin"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # Invalidate Cache File
                temp_dir = tempfile.gettempdir()
                for filename in os.listdir(temp_dir):
                    if filename.endswith('started.lab'):
                        file_path = os.path.join(temp_dir, filename)
                        os.remove(file_path)

            # Finish Process Message
            _Display.info(f"Project '{self.name_app_folder}' successfully created at '{os.path.abspath(project_path)}'.")

        except subprocess.CalledProcessError as e:
            raise ValueError(f"Error while executing command: {e}")

        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")

def main():
    """
    Main entry point for the Flaskavel App Creation Tool.
    Handles argument parsing, validation, and app creation.
    """

    # Startup message
    _Display.welcome()

    # Create the argument parser
    parser = argparse.ArgumentParser(description="Flaskavel App Creation Tool")

    # Required 'new' command and app name
    parser.add_argument('command', choices=['new'], help="Command must be 'new'.")
    parser.add_argument('name_app', help="The name of the Flaskavel application to create.")

    try:

        # Parse the arguments
        args = parser.parse_args()

        # Validate command (this is already done by 'choices')
        if args.command != 'new':
            _Display.error("Unrecognized command, did you mean 'flaskavel new example.app'?")

        # Validate app name (empty check is not needed because argparse handles that)
        if not args.name_app:
            _Display.error("You must specify an application name, did you mean 'flaskavel new example.app'?")

        # Create and run the app
        app = _FlaskavelInit(name_app=args.name_app)
        app.handle()

    except SystemExit as e:
        _Display.error("Invalid arguments. Usage example: 'flaskavel new example_app'")
    except Exception as e:
        _Display.error(f"Fatal Error: {e}")

if __name__ == "__main__":
    main()