from abc import ABC, abstractmethod

class IOutput(ABC):
    """
    Interface for the Output class to ensure consistency in displaying messages to the console.

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

    @abstractmethod
    def welcome(self) -> None:
        """
        Displays a welcome message to the framework.
        """
        pass

    @abstractmethod
    def finished(self) -> None:
        """
        Displays a success message after initialization.
        """
        pass

    @abstractmethod
    def info(self, message: str = '') -> None:
        """
        Displays an informational message to the console.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.
        """
        pass

    @abstractmethod
    def fail(self, message: str = '') -> None:
        """
        Displays a failure message to the console.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.
        """
        pass

    @abstractmethod
    def error(self, message: str = '') -> None:
        """
        Displays an error message to the console and terminates the program.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.
        """
        pass
