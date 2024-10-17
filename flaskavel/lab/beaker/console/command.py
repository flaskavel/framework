import io
import sys
import argparse
from contextlib import redirect_stdout
from flaskavel.lab.beaker.console.output import Console
from flaskavel.lab.beaker.console.progress_bar import ProgressBar

class Command:
    """
    Base class for commands. Commands can inherit from this class
    to access console methods similar to Laravel commands.
    """

    signature = None
    description = "Custom Command Application"

    def __init__(self) -> None:

        # Initialize the argparse parser
        self.argparse = argparse.ArgumentParser(description='Flaskavel Argument Parser')

        # This will store the parsed arguments
        self.args = []
        self.registered_arguments = set()

    def info(self, message:str, timestamp:bool = False):
        """
        Outputs an informational message to the console.

        Args:
            message (str): The message to be displayed.
        """
        Console.info(message, timestamp)

    def error(self, message:str, timestamp:bool = False):
        """
        Outputs an error message to the console.

        Args:
            message (str): The error message to be displayed.
        """
        Console.error(message, timestamp)

    def fail(self, message:str, timestamp:bool = False):
        """
        Outputs a failure message to the console.

        Args:
            message (str): The failure message to be displayed.
        """
        Console.fail(message, timestamp)

    def ask(self, question:str):
        """
        Prompts the user with a question and returns their input.

        Args:
            question (str): The question to be asked.

        Returns:
            str: The user's response.
        """
        return Console.ask(question)

    def confirm(self, question:str):
        """
        Asks the user a yes/no question and returns their confirmation.

        Args:
            question (str): The confirmation question.

        Returns:
            bool: True if the user confirms, False otherwise.
        """
        return Console.confirm(question)

    def secret(self, question:str):
        """
        Asks the user for input in a hidden format (e.g., password).

        Args:
            question (str): The secret question.

        Returns:
            str: The user's input.
        """
        return Console.secret(question)

    def anticipate(self, question:str, options:list, default=None):
        """
        Prompts the user with a question and provides autocomplete options.

        Args:
            question (str): The question to be asked.
            options (list): List of possible options for autocompletion.
            default (str, optional): The default value to return if no match is found.

        Returns:
            str: The user's selected option.
        """
        return Console.anticipate(question, options, default)

    def choice(self, question:str, choices:list, default_index=0):
        """
        Prompts the user with a question and provides a list of choices.

        Args:
            question (str): The question to be asked.
            choices (list): List of choices for the user to select from.
            default_index (int, optional): The default index if the user does not provide an input.

        Returns:
            str: The user's selected choice.
        """
        return Console.choice(question, choices, default_index)

    def line(self, message:str=''):
        """
        Outputs a line of text to the console.

        Args:
            message (str, optional): The message to be displayed. Defaults to an empty string.
        """
        Console.line(message)

    def uniqueLine(self, message:str=''):
        """
        Sends a line of text to the console always erasing any previous content.

        Args:
            message (str, optional): The message to be displayed. Defaults to an empty string.
        """
        Console.clear()
        Console.line(message)

    def newLine(self, count:int=1):
        """
        Outputs a specified number of new lines to the console.

        Args:
            count (int, optional): The number of new lines to be added. Defaults to 1.
        """
        Console.newLine(count)

    def table(self, headers:list, rows:list):
        """
        Outputs a table to the console.

        Args:
            headers (list): The list of table headers.
            rows (list of lists): The list of rows to be displayed in the table.
        """
        Console.table(headers, rows)

    def createProgressBar(self, total:int=100, width:int=50, inline:bool=False):
        """
        Creates a progress bar instance.

        Args:
            total (int, optional): The total number of steps in the progress bar. Defaults to 100.
            width (int, optional): The width of the progress bar. Defaults to 50.
            inline (bool, optional): Whether to display the progress bar inline or clear the console before showing it. Defaults to False.

        Returns:
            ProgressBar: An instance of the ProgressBar class.
        """
        return ProgressBar(total=total, width=width, inline=inline)

    def arguments(self):
        """
        This method should be overridden in child classes to define the arguments.
        Returns a list of tuples where each tuple contains the argument and its options.
        """
        return []

    def _setArguments(self):
        for arg, options in self.arguments():
            if arg not in self.registered_arguments:
                self.argparse.add_argument(arg, **options)
                self.registered_arguments.add(arg)

    def _argumentsParse(self, args):
        """
        Parse the arguments and store them in `self.args`.
        """
        self._setArguments()
        error_msg = 'Parse Argument Error'

        if '-h' in args:
            self.help()

        try:
            self.args = self.argparse.parse_args(args)
        except argparse.ArgumentError as e:
            self.argparse.error(f"{error_msg}: {e}")
        except SystemExit:
            raise ValueError(f"{error_msg}: Please provide all required arguments: {str(',').join(self.registered_arguments)}")

    def help(self):
        """
        Prints the command usage detail.
        """

        # Blank line console
        Console.newLine(1)

        # Extract the console output.
        output = io.StringIO()
        with redirect_stdout(output):
            self.argparse.print_help()
        help_message = output.getvalue()
        output.close()

        Console.line('Help Command Flaskavel')
        Console.info(help_message)
        exit()

    def argument(self, index, default=None):
        """
        Return the value of a given argument by its name.
        """
        if hasattr(self.args, index):
            value = getattr(self.args, index)
            if value is None and default is not None:
                return default
            return value
        else:
            raise ValueError(f"Argument '{index}' not found")

    def handle(self):
        """
        This method should be overridden in specific commands,
        similar to the `handle` method in Laravel commands.
        """
        pass

    def exit(self, code:int=1):
        """
        Exit Command
        """
        sys.exit(code)

    def clean(self):
        """
        Clear the console to print new output.
        """
        Console.clear()