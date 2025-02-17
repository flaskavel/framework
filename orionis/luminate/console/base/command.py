from orionis.luminate.console.output.console import Console
from orionis.luminate.console.output.progress_bar import ProgressBar
from orionis.luminate.contracts.console.base_command_interface import IBaseCommand

class BaseCommand(IBaseCommand):
    """
    A base class for handling common console output functionalities. This class provides methods to print messages of
    various types (success, info, warning, etc.) in different styles (e.g., text, bold, colored).

    This class acts as a foundation for command classes, offering utility methods to interact with the console.
    """

    # Command arguments
    args = {}

    def success(self, message: str = '', timestamp: bool = True):
        """
        Prints a success message with a green background.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        Console.success(message, timestamp)

    def textSuccess(self, message: str = ''):
        """
        Prints a success message in green.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textSuccess(message)

    def textSuccessBold(self, message: str = ''):
        """
        Prints a bold success message in green.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textSuccessBold(message)

    def info(self, message: str = '', timestamp: bool = True):
        """
        Prints an informational message with a blue background.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        Console.info(message, timestamp)

    def textInfo(self, message: str = ''):
        """
        Prints an informational message in blue.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textInfo(message)

    def textInfoBold(self, message: str = ''):
        """
        Prints a bold informational message in blue.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textInfoBold(message)

    def warning(self, message: str = '', timestamp: bool = True):
        """
        Prints a warning message with a yellow background.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        Console.warning(message, timestamp)

    def textWarning(self, message: str = ''):
        """
        Prints a warning message in yellow.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textWarning(message)

    def textWarningBold(self, message: str = ''):
        """
        Prints a bold warning message in yellow.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textWarningBold(message)

    def fail(self, message: str = '', timestamp: bool = True):
        """
        Prints a failure message with a red background.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        Console.fail(message, timestamp)

    def error(self, message: str = '', timestamp: bool = True):
        """
        Prints an error message with a red background.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        Console.error(message, timestamp)

    def textError(self, message: str = ''):
        """
        Prints an error message in red.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textError(message)

    def textErrorBold(self, message: str = ''):
        """
        Prints a bold error message in red.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textErrorBold(message)

    def textMuted(self, message: str = ''):
        """
        Prints a muted (gray) message.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textMuted(message)

    def textMutedBold(self, message: str = ''):
        """
        Prints a bold muted (gray) message.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textMutedBold(message)

    def textUnderline(self, message: str = ''):
        """
        Prints an underlined message.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.textUnderline(message)

    def clear(self):
        """
        Clears the console screen.
        """
        Console.clear()

    def clearLine(self):
        """
        Clears the current console line.
        """
        Console.clearLine()

    def line(self, message: str = ''):
        """
        Prints a line of text.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.line(message)

    def newLine(self, count: int = 1):
        """
        Prints multiple new lines.

        Parameters
        ----------
        count : int, optional
            The number of new lines to print (default is 1).
        """
        Console.newLine(count)

    def write(self, message: str = ''):
        """
        Prints a message without moving to the next line.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.write(message)

    def writeLine(self, message: str = ''):
        """
        Prints a message and moves to the next line.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        Console.writeLine(message)

    def ask(self, question: str) -> str:
        """
        Prompts the user for input and returns the response.

        Parameters
        ----------
        question : str
            The question to ask the user.

        Returns
        -------
        str
            The user's input.
        """
        return Console.ask(question)

    def confirm(self, question: str, default: bool = False) -> bool:
        """
        Asks a confirmation question and returns True/False based on the user's response.

        Parameters
        ----------
        question : str
            The confirmation question to ask.
        default : bool, optional
            The default response if the user presses Enter without typing a response (default is False).

        Returns
        -------
        bool
            The user's response.
        """
        return Console.ask(question, default)

    def secret(self, question: str) -> str:
        """
        Prompts for hidden input (e.g., password).

        Parameters
        ----------
        question : str
            The prompt to ask the user.

        Returns
        -------
        str
            The user's hidden input.
        """
        return Console.secret(question)

    def table(self, headers: list, rows: list):
        """
        Prints a formatted table in the console.

        Parameters
        ----------
        headers : list of str
            The column headers for the table.
        rows : list of list of str
            The rows of the table.

        Raises
        ------
        ValueError
            If headers or rows are empty.
        """
        Console.table(headers, rows)

    def anticipate(self, question: str, options: list, default=None):
        """
        Provides autocomplete suggestions for user input.

        Parameters
        ----------
        question : str
            The prompt for the user.
        options : list of str
            The list of possible options for autocomplete.
        default : str, optional
            The default value if no matching option is found (default is None).

        Returns
        -------
        str
            The chosen option or the default value.
        """
        Console.anticipate(question, options, default)

    def choice(self, question: str, choices: list, default_index: int = 0) -> str:
        """
        Prompts the user to select a choice from a list.

        Parameters
        ----------
        question : str
            The prompt for the user.
        choices : list of str
            The list of available choices.
        default_index : int, optional
            The index of the default choice (default is 0).

        Returns
        -------
        str
            The selected choice.

        Raises
        ------
        ValueError
            If `default_index` is out of the range of choices.
        """
        Console.choice(question, choices, default_index)

    def createProgressBar(self, total: int = 100, width: int = 50) -> ProgressBar:
        """
        Creates and returns a new progress bar.

        This method initializes a `ProgressBar` object with the specified total and width.

        Parameters
        ----------
        total : int, optional
            The total number of steps for the progress bar. Default is 100.
        width : int, optional
            The width (in characters) of the progress bar. Default is 50.

        Returns
        -------
        ProgressBar
            A new instance of the `ProgressBar` class, initialized with the specified `total` and `width`.

        Notes
        -----
        The progress bar can be used to visually track the progress of a task.
        The `total` parameter represents the number of steps to complete the task,
        and the `width` parameter controls the number of characters used to represent the progress bar in the console.
        """
        return ProgressBar(total=total, width=width)

    def setArgs(self, args):
        """
        Define the logic of setting command arguments.

        Parameters
        ----------
        args : argparse.Namespace
            Contain the arguments to be set for the command.
        """
        try:
            # Convert arguments to a dictionary using vars(), if possible
            self.args = vars(args)
        except TypeError:
            # Fallback to an empty dictionary if args is not compatible with vars()
            self.args = {}


    def handle(self, **kwargs):
        """
        Abstract method to define the logic of the command.

        This method must be overridden in subclasses.

        Arguments:
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass. This ensures that all command classes
                                adhere to the expected structure.
        """
        raise NotImplementedError("The 'handle' method must be implemented in the child class.")