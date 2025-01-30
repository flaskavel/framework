import os
import sys
import datetime
from flaskavel.metadata import NAME, VERSION, DOCS
from flaskavel.luminate.contracts.installer.output_interface import IOutput

class Output(IOutput):
    """
    Class for specific use within this file.
    Provides static methods to display messages to the console,
    such as welcome messages, informational messages, failure messages, and error messages.

    Attributes
    ----------
    None

    Methods
    -------
    welcome()
        Displays a welcome message to the framework.
    finished()
        Displays a success message after initialization.
    info(message: str)
        Displays an informational message to the console.
    fail(message: str)
        Displays a failure message to the console.
    error(message: str)
        Displays an error message to the console and terminates the program.
    """

    @staticmethod
    def write(label: str, message: str, color_code: str):
        """
        Private method to print messages in the console with specific formatting and colors.

        Parameters
        ----------
        label : str
            The label for the message (INFO, FAIL, ERROR).
        message : str
            The message to display.
        color_code : str
            ANSI color code for the background of the message.

        Returns
        -------
        None
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'\u001b[{color_code}m\u001b[97m {label} \u001b[0m {timestamp} [Init Project] - {message}\u001b[0m')

    @staticmethod
    def welcome():
        """
        Displays a welcome message to the framework.

        This method does not take any parameters and does not return any value.

        Returns
        -------
        None
        """
        print("\n")

        # Print ASCII Art
        try:
            dir_path = os.path.dirname(__file__)
            path = os.path.join(dir_path, 'art.ascii')
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            year = datetime.datetime.now().year
            message = '\u001b[32m{} \u001b[0m'.format("Python isn't just powerful; it’s thrilling.")
            output = content.replace('{{version}}', str(VERSION)).replace('{{docs}}', DOCS).replace('{{year}}', str(year)).replace('{{message}}', str(message))
            print(output)
        except FileNotFoundError:
            print(str(NAME).upper())
            print(f"Version: {str(VERSION)}")
            print(f"Docs: {DOCS}")

        print("\n")

        # Displays a success message.
        print('\u001b[32m{} \u001b[0m'.format(f"Thank you for using {NAME}."))

    @staticmethod
    def finished():
        """
        Displays a welcome message to the framework.

        This method does not take any parameters and does not return any value.

        Returns
        -------
        None
        """
        # Displays a success message.
        print('\u001b[32m{} \u001b[0m'.format("Welcome aboard, the journey starts now. Let your imagination soar!"))
        print("\n")

    @staticmethod
    def info(message: str = ''):
        """
        Displays an informational message to the console.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.

        Returns
        -------
        None
        """
        Output.write("INFO", message, "44")

    @staticmethod
    def fail(message: str = ''):
        """
        Displays a failure message to the console.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.

        Returns
        -------
        None
        """
        Output.write("FAIL", message, "43")

    @staticmethod
    def error(message: str = ''):
        """
        Displays an error message to the console and terminates the program.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.

        Returns
        -------
        None

        Raises
        ------
        SystemExit
            Terminates the program with a non-zero exit code.
        """
        Output.write("ERROR", message, "41")
        print("\n")
        sys.exit(1)
