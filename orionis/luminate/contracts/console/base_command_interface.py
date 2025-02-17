from abc import ABC, abstractmethod
from typing import List

from orionis.luminate.console.output.progress_bar import ProgressBar

class IBaseCommand(ABC):
    """
    Interface for console output commands. This defines the methods that must be implemented in a command class.
    """

    @abstractmethod
    def success(self, message: str = '', timestamp: bool = True) -> None:
        """
        Prints a success message with a green background.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        pass

    @abstractmethod
    def textSuccess(self, message: str = '') -> None:
        """
        Prints a success message in green.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def textSuccessBold(self, message: str = '') -> None:
        """
        Prints a bold success message in green.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def info(self, message: str = '', timestamp: bool = True) -> None:
        """
        Prints an informational message with a blue background.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        pass

    @abstractmethod
    def textInfo(self, message: str = '') -> None:
        """
        Prints an informational message in blue.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def textInfoBold(self, message: str = '') -> None:
        """
        Prints a bold informational message in blue.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def warning(self, message: str = '', timestamp: bool = True) -> None:
        """
        Prints a warning message with a yellow background.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        pass

    @abstractmethod
    def textWarning(self, message: str = '') -> None:
        """
        Prints a warning message in yellow.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def textWarningBold(self, message: str = '') -> None:
        """
        Prints a bold warning message in yellow.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def fail(self, message: str = '', timestamp: bool = True) -> None:
        """
        Prints a failure message with a red background.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        pass

    @abstractmethod
    def error(self, message: str = '', timestamp: bool = True) -> None:
        """
        Prints an error message with a red background.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        timestamp : bool, optional
            Whether to include a timestamp (default is True).
        """
        pass

    @abstractmethod
    def textError(self, message: str = '') -> None:
        """
        Prints an error message in red.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def textErrorBold(self, message: str = '') -> None:
        """
        Prints a bold error message in red.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def textMuted(self, message: str = '') -> None:
        """
        Prints a muted (gray) message.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def textMutedBold(self, message: str = '') -> None:
        """
        Prints a bold muted (gray) message.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def textUnderline(self, message: str = '') -> None:
        """
        Prints an underlined message.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clears the console screen.
        """
        pass

    @abstractmethod
    def clearLine(self) -> None:
        """
        Clears the current console line.
        """
        pass

    @abstractmethod
    def line(self, message: str = '') -> None:
        """
        Prints a line of text.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def newLine(self, count: int = 1) -> None:
        """
        Prints multiple new lines.

        Parameters
        ----------
        count : int, optional
            The number of new lines to print (default is 1).
        """
        pass

    @abstractmethod
    def write(self, message: str = '') -> None:
        """
        Prints a message without moving to the next line.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
    def writeLine(self, message: str = '') -> None:
        """
        Prints a message and moves to the next line.

        Parameters
        ----------
        message : str, optional
            The message to display (default is an empty string).
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def table(self, headers: List[str], rows: List[List[str]]) -> None:
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
        pass

    @abstractmethod
    def anticipate(self, question: str, options: List[str], default=None) -> str:
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
        pass

    @abstractmethod
    def choice(self, question: str, choices: List[str], default_index: int = 0) -> str:
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def setArgs(self, args) -> None:
        """
        Abstract method to define the logic of setting command arguments.

        Parameters
        ----------
        args : argparse.Namespace
            Contain the arguments to be set for the command.
        """
        pass

    @abstractmethod
    def handle(self, *args, **kwargs):
        """
        Abstract method to define the logic of the command.

        This method must be overridden in subclasses.

        Arguments:
            *args: A list of variable-length arguments.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass. This ensures that all command classes
                                adhere to the expected structure.
        """
        pass
