import os
import getpass
from flaskavel.lab.catalyst.colors import ConsoleColor
from flaskavel.lab.beaker.console.helpers import strftime

class Console:

    @staticmethod
    def clear():
        """Clears the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def executeTimestamp(command: str, state: str, seconds: str = ''):
        """
        Prints the command execution status with a timestamp.

        Args:
            command (str): The command being executed.
            state (str): The state of the command (RUNNING, DONE, or FAIL).
            seconds (str, optional): Additional time information. Defaults to an empty string.

        Raises:
            ValueError: If the provided state is not supported.
        """
        states = ['RUNNING', 'DONE', 'FAIL']
        if state not in states:
            raise ValueError("State not supported.")

        width = 60
        len_str = len(state)
        len_seconds = len(seconds)

        line = '.' * (width - (len_str + len_seconds))

        # Colorize state based on its value
        if state == 'RUNNING':
            state = f"{ConsoleColor.YELLOW_BOLD.value}RUNNING{ConsoleColor.DEFAULT.value}"
        elif state == 'DONE':
            state = f"{ConsoleColor.GREEN_BOLD.value}DONE{ConsoleColor.DEFAULT.value}"
        elif state == 'FAIL':
            state = f"{ConsoleColor.RED_BOLD.value}FAIL{ConsoleColor.DEFAULT.value}"

        # Print the formatted message
        print(f"{ConsoleColor.MUTED.value}{strftime()}{ConsoleColor.DEFAULT.value} {command} {line} "
              f"{ConsoleColor.MUTED.value}{seconds}{ConsoleColor.DEFAULT.value} {state}")

    @staticmethod
    def error(message: str = '', timestamp: bool = False):
        """
        Prints an error message in red.

        Args:
            message (str, optional): The error message to print. Defaults to an empty string.
            timestamp (bool, optional): Whether to include a timestamp. Defaults to False.
        """
        str_time = f"{ConsoleColor.MUTED.value}{strftime()}{ConsoleColor.DEFAULT.value}" if timestamp else ''
        print(f"{ConsoleColor.ERROR_COLOR_BG.value}{ConsoleColor.WHITE.value} ERROR {ConsoleColor.DEFAULT.value} "
              f"{str_time} {message}{ConsoleColor.DEFAULT.value}")

    @staticmethod
    def textDanger(message: str = ''):
        """
        Prints a danger message in red.

        Args:
            message (str, optional): The danger message to print. Defaults to an empty string.
        """
        print(f"{ConsoleColor.RED_BOLD.value}{message}{ConsoleColor.DEFAULT.value}")

    @staticmethod
    def textSuccess(message: str = ''):
        """
        Prints a success message in green.

        Args:
            message (str, optional): The success message to print. Defaults to an empty string.
        """
        print(f"{ConsoleColor.GREEN_BOLD.value}{message}{ConsoleColor.DEFAULT.value}")

    @staticmethod
    def textWarning(message: str = ''):
        """
        Prints a warning message in yellow.

        Args:
            message (str, optional): The warning message to print. Defaults to an empty string.
        """
        print(f"{ConsoleColor.YELLOW_BOLD.value}{message}{ConsoleColor.DEFAULT.value}")

    @staticmethod
    def fail(message: str = '', timestamp: bool = False):
        """
        Prints a failure message in red.

        Args:
            message (str, optional): The failure message to print. Defaults to an empty string.
            timestamp (bool, optional): Whether to include a timestamp. Defaults to False.
        """
        str_time = f"{ConsoleColor.MUTED.value}{strftime()}{ConsoleColor.DEFAULT.value}" if timestamp else ''
        print(f"{ConsoleColor.ERROR_COLOR_BG.value}{ConsoleColor.WHITE.value} FAIL {ConsoleColor.DEFAULT.value} "
              f"{str_time} {message}{ConsoleColor.DEFAULT.value}")

    @staticmethod
    def info(message: str = '', timestamp: bool = False):
        """
        Prints an informational message in blue.

        Args:
            message (str, optional): The informational message to print. Defaults to an empty string.
            timestamp (bool, optional): Whether to include a timestamp. Defaults to False.
        """
        str_time = f"{ConsoleColor.MUTED.value}{strftime()}{ConsoleColor.DEFAULT.value}" if timestamp else ''
        print(f"{ConsoleColor.INFO_COLOR_BG.value}{ConsoleColor.WHITE.value} INFO {ConsoleColor.DEFAULT.value} "
              f"{str_time} {message}{ConsoleColor.DEFAULT.value}")

    @staticmethod
    def ask(question: str):
        """
        Prompts the user for input with a message.

        Args:
            question (str): The question to ask the user.

        Returns:
            str: The user's input.
        """
        return input(f"{ConsoleColor.INFO_COLOR.value}{str(question).strip()}{ConsoleColor.DEFAULT.value} ")

    @staticmethod
    def confirm(question: str, default: bool = False):
        """
        Asks a confirmation question and returns True or False.

        Args:
            question (str): The confirmation question.
            default (bool, optional): The default response if the user just presses Enter. Defaults to False.

        Returns:
            bool: The user's response (True if 'Y', False if 'N').
        """
        response = input(f"{ConsoleColor.INFO_COLOR.value}{str(question).strip()} (Y/n): {ConsoleColor.DEFAULT.value} ").upper()
        return default if not response else response == 'Y'

    @staticmethod
    def secret(question: str):
        """
        Prompts for hidden input from the user, such as a password.

        Args:
            question (str): The prompt for the user.

        Returns:
            str: The user's hidden input.
        """
        return getpass.getpass(f"{ConsoleColor.INFO_COLOR.value}{str(question).strip()}{ConsoleColor.DEFAULT.value} ")

    @staticmethod
    def anticipate(question: str, options: list, default=None):
        """
        Provides autocomplete suggestions based on user input.

        Args:
            question (str): The prompt for the user.
            options (list of str): The list of options for autocomplete.
            default (str, optional): The default value if no matching option is found. Defaults to None.

        Returns:
            str: The chosen option or the default value.
        """
        input_value = input(f"{ConsoleColor.INFO_COLOR.value}{str(question).strip()}{ConsoleColor.DEFAULT.value} ")
        return next((option for option in options if option.startswith(input_value)), default or input_value)

    @staticmethod
    def choice(question: str, choices: list, default_index=0):
        """
        Allows the user to select an option from a list.

        Args:
            question (str): The prompt for the user.
            choices (list of str): The list of choices.
            default_index (int, optional): The index of the default choice. Defaults to 0.

        Returns:
            str: The selected choice.
        """
        total_choices = len(choices)

        print(f"{ConsoleColor.INFO_COLOR.value}{str(question).strip()} (default: {choices[default_index]}): {ConsoleColor.DEFAULT.value} ")
        for idx, choice in enumerate(choices, 1):
            print(f"{idx}: {choice}")

        answer = input("Answer: ")
        while not answer.isnumeric() or not (1 <= int(answer) <= total_choices):
            answer = input("Please select a valid number: ")

        return choices[int(answer) - 1]

    @staticmethod
    def line(message: str = ''):
        """
        Prints a line of text.

        Args:
            message (str, optional): The message to print. Defaults to an empty string.
        """
        print(message)

    @staticmethod
    def newLine(count: int = 1):
        """
        Prints multiple new lines.

        Args:
            count (int, optional): The number of new lines to print. Defaults to 1.

        Raises:
            ValueError: If count is less than or equal to 0.
        """
        if count <= 0:
            raise ValueError(f"Unsupported Value '{str(count)}'")
        print("\n" * count)

    @staticmethod
    def table(headers: list, rows: list):
        """
        Prints a table in the console.

        Args:
            headers (list of str): The column headers.
            rows (list of lists of str): The rows of the table.
        """
        # Determine column widths
        col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]
        header_row = " | ".join(f"{header:<{col_width}}" for header, col_width in zip(headers, col_widths))
        separator = "-+-".join("-" * col_width for col_width in col_widths)

        # Print the table
        print(header_row)
        print(separator)
        for row in rows:
            print(" | ".join(f"{item:<{col_width}}" for item, col_width in zip(row, col_widths)))
