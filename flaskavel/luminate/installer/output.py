import os
import sys
import datetime
from flaskavel.metadata import NAME, VERSION, DOCS
from flaskavel.luminate.contracts.installer.output_interface import IOutput

class Output(IOutput):
    """
    Class for displaying various types of messages to the console, including:
    - Welcome messages
    - Informational messages
    - Failure messages
    - Error messages

    Methods
    -------
    welcome() -> None
        Displays a welcome message to the framework.
    finished() -> None
        Displays a success message after initialization.
    info(message: str) -> None
        Displays an informational message to the console.
    fail(message: str) -> None
        Displays a failure message to the console.
    error(message: str) -> None
        Displays an error message to the console and terminates the program.
    """

    @staticmethod
    def _print(label: str, message: str, color_code: str):
        """
        Prints messages to the console with specific formatting and colors.

        Parameters
        ----------
        label : str
            The label for the message (e.g., INFO, FAIL, ERROR).
        message : str
            The message to display.
        color_code : str
            ANSI color code for the background of the message.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'\u001b[{color_code}m\u001b[97m {label} \u001b[0m {timestamp} [Flaskavel Framework] - {message}\u001b[0m')

    @staticmethod
    def asciiArt():
        """
        Displays a welcome message to the framework, including ASCII art.

        Attempts to load an ASCII art file (art.ascii). If not found, defaults to displaying basic information.
        """
        print("\n")

        try:
            # Try loading and printing ASCII art from file
            dir_path = os.path.dirname(__file__)
            path = os.path.join(dir_path, 'art.ascii')
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Replace placeholders with dynamic content
            year = datetime.datetime.now().year
            message = '\u001b[32m{} \u001b[0m'.format("Python isn't just powerful; it’s thrilling.")
            output = content.replace('{{version}}', VERSION) \
                            .replace('{{docs}}', DOCS) \
                            .replace('{{year}}', str(year)) \
                            .replace('{{message}}', message)
            print(output)

        except FileNotFoundError:
            # Fallback if ASCII art file is not found
            print(str(NAME).upper())
            print(f"Version: {VERSION}")
            print(f"Docs: {DOCS}")

        print("\n")

    @staticmethod
    def startInstallation():
        """
        Displays the starting message when installation begins.
        """
        Output.asciiArt()
        print(f'\u001b[32m{NAME}\u001b[0m: Thank you for using the framework!')

    @staticmethod
    def endInstallation():
        """
        Displays the ending message after installation is complete.
        """
        print(f'\u001b[32m{NAME}\u001b[0m: Welcome aboard, the journey starts now. Let your imagination soar!')
        print("\n")

    @staticmethod
    def info(message: str = ''):
        """
        Displays an informational message to the console.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.
        """
        Output._print("INFO", message, "44")

    @staticmethod
    def fail(message: str = ''):
        """
        Displays a failure message to the console.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.
        """
        Output._print("FAIL", message, "43")

    @staticmethod
    def error(message: str = ''):
        """
        Displays an error message to the console and terminates the program.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.

        Raises
        ------
        SystemExit
            Terminates the program with a non-zero exit code.
        """
        Output._print("ERROR", message, "41")
        print("\n")
        sys.exit(1)
