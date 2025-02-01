import getpass
import os
import sys
import datetime
from flaskavel.luminate.console.output.styles import ANSIColors
from flaskavel.luminate.contracts.console.console_interface import IConsole

class Console(IConsole):
    """
    Utility class for printing formatted messages to the console with ANSI colors.

    Provides methods to print success, info, warning, and error messages with
    optional timestamps, as well as general text formatting methods.
    """

    @staticmethod
    def _get_timestamp() -> str:
        """
        Returns the current date and time formatted in a muted color.

        Returns
        -------
        str
            The formatted timestamp with muted color.
        """
        return f"{ANSIColors.TEXT_MUTED.value}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{ANSIColors.DEFAULT.value}"

    @staticmethod
    def _print_with_background(label: str, bg_color: ANSIColors, message: str, timestamp: bool):
        """
        Prints a formatted message with a background color.

        Parameters
        ----------
        label : str
            The label to display (e.g., 'SUCCESS', 'INFO').
        bg_color : ANSIColors
            The background color to use.
        message : str
            The message to print.
        timestamp : bool
            Whether to include a timestamp.
        """
        str_time = Console._get_timestamp() if timestamp else ''
        print(f"{bg_color.value}{ANSIColors.TEXT_WHITE.value} {label} {ANSIColors.DEFAULT.value} {str_time} {message}{ANSIColors.DEFAULT.value}")

    @staticmethod
    def _print_colored(message: str, text_color: ANSIColors):
        """
        Prints a message with a specified text color.

        Parameters
        ----------
        message : str
            The message to print.
        text_color : ANSIColors
            The text color to use.
        """
        print(f"{text_color.value}{message}{ANSIColors.DEFAULT.value}")

    # ---- SUCCESS ----

    @staticmethod
    def success(message: str = '', timestamp: bool = True):
        """
        Prints a success message with a green background.

        Parameters
        ----------
        message : str, optional
            The success message to print (default is '').
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        Console._print_with_background("SUCCESS", ANSIColors.BG_SUCCESS, message, timestamp)

    @staticmethod
    def textSuccess(message: str = ''):
        """Prints a success message in green."""
        Console._print_colored(message, ANSIColors.TEXT_SUCCESS)

    @staticmethod
    def textSuccessBold(message: str = ''):
        """Prints a bold success message in green."""
        Console._print_colored(message, ANSIColors.TEXT_BOLD_SUCCESS)

    # ---- INFO ----

    @staticmethod
    def info(message: str = '', timestamp: bool = True):
        """Prints an informational message with a blue background."""
        Console._print_with_background("INFO", ANSIColors.BG_INFO, message, timestamp)

    @staticmethod
    def textInfo(message: str = ''):
        """Prints an informational message in blue."""
        Console._print_colored(message, ANSIColors.TEXT_INFO)

    @staticmethod
    def textInfoBold(message: str = ''):
        """Prints a bold informational message in blue."""
        Console._print_colored(message, ANSIColors.TEXT_BOLD_INFO)

    # ---- WARNING ----

    @staticmethod
    def warning(message: str = '', timestamp: bool = True):
        """Prints a warning message with a yellow background."""
        Console._print_with_background("WARNING", ANSIColors.BG_WARNING, message, timestamp)

    @staticmethod
    def textWarning(message: str = ''):
        """Prints a warning message in yellow."""
        Console._print_colored(message, ANSIColors.TEXT_WARNING)

    @staticmethod
    def textWarningBold(message: str = ''):
        """Prints a bold warning message in yellow."""
        Console._print_colored(message, ANSIColors.TEXT_BOLD_WARNING)

    # ---- FAIL ----

    @staticmethod
    def fail(message: str = '', timestamp: bool = True):
        """Prints an error message with a red background."""
        Console._print_with_background("FAIL", ANSIColors.BG_FAIL, message, timestamp)

    # ---- ERROR ----

    @staticmethod
    def error(message: str = '', timestamp: bool = True):
        """Prints an error message with a red background."""
        Console._print_with_background("ERROR", ANSIColors.BG_ERROR, message, timestamp)

    @staticmethod
    def textError(message: str = ''):
        """Prints an error message in red."""
        Console._print_colored(message, ANSIColors.TEXT_ERROR)

    @staticmethod
    def textErrorBold(message: str = ''):
        """Prints a bold error message in red."""
        Console._print_colored(message, ANSIColors.TEXT_BOLD_ERROR)

    # ---- MUTED ----

    @staticmethod
    def textMuted(message: str = ''):
        """Prints a muted (gray) message."""
        Console._print_colored(message, ANSIColors.TEXT_MUTED)

    @staticmethod
    def textMutedBold(message: str = ''):
        """Prints a bold muted (gray) message."""
        Console._print_colored(message, ANSIColors.TEXT_BOLD_MUTED)

    # ---- UNDERLINE ----

    @staticmethod
    def textUnderline(message: str = ''):
        """
        Prints an underlined message.

        Parameters
        ----------
        message : str, optional
            The message to print (default is '').
        """
        print(f"{ANSIColors.TEXT_STYLE_UNDERLINE.value}{message}{ANSIColors.DEFAULT.value}")

    # ---- CLEAR CONSOLE ----

    @staticmethod
    def clear():
        """Clears the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def clearLine():
        """Clears the current console line."""
        sys.stdout.write("\r \r")
        sys.stdout.flush()

    # ---- EMPTY LINE CONSOLE ----

    @staticmethod
    def line(message: str = ''):
        """Prints a line of text."""
        print(message)

    @staticmethod
    def newLine(count: int = 1):
        """
        Prints multiple new lines.

        Parameters
        ----------
        count : int, optional
            The number of new lines to print (default is 1).

        Raises
        ------
        ValueError
            If count is less than or equal to 0.
        """
        if count <= 0:
            raise ValueError(f"Unsupported Value '{count}'")
        print("\n" * count, end="")

    # ---- WRITE CONSOLE ----

    @staticmethod
    def write(message: str = ''):
        """
        Prints a message without moving to the next line.

        Parameters
        ----------
        message : str, optional
            The message to print (default is '').
        """
        sys.stdout.write(f"{message}")
        sys.stdout.flush()

    @staticmethod
    def writeLine(message: str = ''):
        """
        Prints a message and moves to the next line.

        Parameters
        ----------
        message : str, optional
            The message to print (default is '').
        """
        print(f"{message}")

    @staticmethod
    def ask(question: str) -> str:
        """
        Prompts the user for input with a message and returns the user's response.

        Parameters
        ----------
        question : str
            The question to ask the user.

        Returns
        -------
        str
            The user's input, as a string.
        """
        return input(f"{ANSIColors.TEXT_INFO.value}{str(question).strip()}{ANSIColors.DEFAULT.value} ")

    @staticmethod
    def confirm(question: str, default: bool = False) -> bool:
        """
        Asks a confirmation question and returns True or False based on the user's response.

        Parameters
        ----------
        question : str
            The confirmation question to ask.
        default : bool, optional
            The default response if the user presses Enter without typing a response.
            Default is False, which corresponds to a 'No' response.

        Returns
        -------
        bool
            The user's response, which will be True if 'Y' is entered,
            or False if 'N' is entered or the default is used.
        """
        response = input(f"{ANSIColors.TEXT_INFO.value}{str(question).strip()} (Y/n): {ANSIColors.DEFAULT.value} ").upper()
        return default if not response else response == 'Y'

    @staticmethod
    def secret(question: str) -> str:
        """
        Prompts the user for hidden input, typically used for password input.

        Parameters
        ----------
        question : str
            The prompt to ask the user.

        Returns
        -------
        str
            The user's hidden input, returned as a string.
        """
        return getpass.getpass(f"{ANSIColors.TEXT_INFO.value}{str(question).strip()}{ANSIColors.DEFAULT.value} ")

    @staticmethod
    def table(headers: list, rows: list):
        """
        Prints a table in the console with the given headers and rows, with bold headers.

        Parameters
        ----------
        headers : list of str
            The column headers for the table.
        rows : list of list of str
            The rows of the table, where each row is a list of strings representing the columns.

        Raises
        ------
        ValueError
            If headers or rows are empty.

        Notes
        -----
        The table adjusts column widths dynamically, includes bold headers, and uses box-drawing characters for formatting.
        """
        if not headers:
            raise ValueError("Headers cannot be empty.")
        if not rows:
            raise ValueError("Rows cannot be empty.")

        # Determine the maximum width of each column
        col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]

        # Define border characters
        top_border = "┌" + "┬".join("─" * (col_width + 2) for col_width in col_widths) + "┐"
        separator = "├" + "┼".join("─" * (col_width + 2) for col_width in col_widths) + "┤"
        bottom_border = "└" + "┴".join("─" * (col_width + 2) for col_width in col_widths) + "┘"

        # Format the header row with bold text
        header_row = "│ " + " │ ".join(f"{ANSIColors.TEXT_BOLD.value}{header:<{col_width}}{ANSIColors.TEXT_RESET.value}" for header, col_width in zip(headers, col_widths)) + " │"

        # Print the table
        print(top_border)
        print(header_row)
        print(separator)

        for row in rows:
            row_text = "│ " + " │ ".join(f"{str(item):<{col_width}}" for item, col_width in zip(row, col_widths)) + " │"
            print(row_text)

        print(bottom_border)

    @staticmethod
    def anticipate(question: str, options: list, default=None):
        """
        Provides autocomplete suggestions based on user input.

        Parameters
        ----------
        question : str
            The prompt for the user.
        options : list of str
            The list of possible options for autocomplete.
        default : str, optional
            The default value if no matching option is found. Defaults to None.

        Returns
        -------
        str
            The chosen option or the default value.

        Notes
        -----
        This method allows the user to input a string, and then attempts to provide
        an autocomplete suggestion by matching the beginning of the input with the
        available options. If no match is found, the method returns the default value
        or the user input if no default is provided.
        """
        # Prompt the user for input
        input_value = input(f"{ANSIColors.TEXT_INFO.value}{str(question).strip()}{ANSIColors.DEFAULT.value} ")

        # Find the first option that starts with the input value, or use the default value
        return next((option for option in options if option.startswith(input_value)), default or input_value)

    @staticmethod
    def choice(question: str, choices: list, default_index: int = 0) -> str:
        """
        Allows the user to select an option from a list.

        Parameters
        ----------
        question : str
            The prompt for the user.
        choices : list of str
            The list of available choices.
        default_index : int, optional
            The index of the default choice (zero-based). Defaults to 0.

        Returns
        -------
        str
            The selected choice.

        Raises
        ------
        ValueError
            If `default_index` is out of the range of choices.

        Notes
        -----
        The user is presented with a numbered list of choices and prompted to select
        one by entering the corresponding number. If an invalid input is provided,
        the user will be repeatedly prompted until a valid choice is made.
        """
        if not choices:
            raise ValueError("The choices list cannot be empty.")

        if not (0 <= default_index < len(choices)):
            raise ValueError(f"Invalid default_index {default_index}. Must be between 0 and {len(choices) - 1}.")

        # Display the question and the choices
        print(f"{ANSIColors.TEXT_INFO.value}{question.strip()} (default: {choices[default_index]}):{ANSIColors.DEFAULT.value}")

        for idx, choice in enumerate(choices, 1):
            print(f"{ANSIColors.TEXT_MUTED.value}{idx}: {choice}{ANSIColors.DEFAULT.value}")

        # Prompt the user for input
        answer = input("Answer: ").strip()

        # If the user provides no input, select the default choice
        if not answer:
            return choices[default_index]

        # Validate input: ensure it's a number within range
        while not answer.isdigit() or not (1 <= int(answer) <= len(choices)):
            answer = input("Please select a valid number: ").strip()

        return choices[int(answer) - 1]
