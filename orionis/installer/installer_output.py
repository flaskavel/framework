import os
import sys
import datetime
import traceback
from orionis.contracts.installer.i_installer_output import IInstallerOutput
from orionis.framework import NAME, VERSION, DOCS

class InstallerOutput(IInstallerOutput):
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
        # Get the current timestamp to display with the message
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print the formatted message with the specified color and label
        print(f'\u001b[{color_code}m\u001b[97m {label} \u001b[0m {timestamp} [Orionis Framework] - {message}\u001b[0m')

    @staticmethod
    def asciiIco():
        """
        Displays a welcome message to the framework, including ASCII art.

        Attempts to load an ASCII art file (art.ascii). If not found, defaults to displaying basic information.

        If the ASCII art file is found, placeholders are replaced with dynamic content such as version, docs, and year.
        """

        try:
            # Try loading and printing ASCII art from the file
            dir_path = os.path.dirname(__file__)
            path = os.path.join(dir_path, '..', 'static', 'ascii', 'icon.ascii')
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Replace placeholders with dynamic content
            year = datetime.datetime.now().year
            message = "\u001b[32m{} \u001b[0m".format("Python isn't just powerful; it’s thrilling.")
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

    @staticmethod
    def asciiInfo():
        """
        Displays another type of welcome message to the framework, including different ASCII art.

        Attempts to load an ASCII art file (info.ascii). If not found, defaults to displaying basic information.

        Similar to `asciiIco()`, but with different ASCII art.
        """
        try:
            # Try loading and printing ASCII art from the file
            dir_path = os.path.dirname(__file__)
            path = os.path.join(dir_path, '..', 'static', 'ascii', 'info.ascii')
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Replace placeholders with dynamic content
            year = datetime.datetime.now().year
            message = "\033[92m{} \033[0m".format("The list of commands accepted by the Orionis interpreter are:")
            commands = [
                {'name':'orionis new <app_name>', 'description': 'Creates a new Orionis app with the specified name.'},
                {'name':'orionis --version', 'description': 'Displays the current version of Orionis.'},
                {'name':'orionis --upgrade', 'description': 'Upgrades Orionis to the latest version.'}
            ]
            commands_array = []
            for command in commands:
                commands_array.append("\033[1m\033[93m- {} :\033[0m {}".format(command['name'],command['description']))

            output = content.replace('{{version}}', VERSION) \
                            .replace('{{docs}}', DOCS) \
                            .replace('{{year}}', str(year))\
                            .replace('{{message}}', message)\
                            .replace('{{commands}}', str("\n").join(commands_array))
            print(output)

        except FileNotFoundError:
            # Fallback if ASCII art file is not found
            print(str(NAME).upper())
            print(f"Version: {VERSION}")
            print(f"Docs: {DOCS}")

    @staticmethod
    def startInstallation():
        """
        Displays the starting message when the installation begins.
        This includes a welcoming message and the ASCII art.
        """
        InstallerOutput.asciiIco()
        print(f'\u001b[32mThank you for using the framework!\u001b[0m')

    @staticmethod
    def endInstallation():
        """
        Displays the ending message after the installation is complete.
        Provides a message of encouragement to start using the framework.
        """
        print(f'\u001b[32mWelcome aboard, the journey starts now. Let your imagination soar!\u001b[0m')
        print("-------------------------------------------")

    @staticmethod
    def info(message: str = ''):
        """
        Displays an informational message to the console.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.
        """
        InstallerOutput._print("INFO", message, "44")

    @staticmethod
    def fail(message: str = ''):
        """
        Displays a failure message to the console.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.
        """
        InstallerOutput._print("FAIL", message, "43")

    @staticmethod
    def error(message: str = '', e = None):
        """
        Displays an error message to the console and terminates the program.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.

        Raises
        ------
        SystemExit
            Terminates the program with a non-zero exit code, indicating an error occurred.
        """

        InstallerOutput._print("ERROR", message, "41")

        if isinstance(e, BaseException):
            print("\n--- Traceback (most recent call last) ---")
            traceback.print_exc()

        sys.exit(1)
