from abc import ABC, abstractmethod

class IOutput(ABC):
    """
    Interface for Output class to ensure the implementation of methods for displaying
    various messages to the console, including:
    - Welcome messages
    - Informational messages
    - Failure messages
    - Error messages
    """

    @staticmethod
    @abstractmethod
    def asciiArt() -> None:
        """
        Displays a welcome message to the framework, including ASCII art.
        """
        pass

    @staticmethod
    @abstractmethod
    def startInstallation() -> None:
        """
        Displays the starting message when installation begins.
        """
        pass

    @staticmethod
    @abstractmethod
    def endInstallation() -> None:
        """
        Displays the ending message after installation is complete.
        """
        pass

    @staticmethod
    @abstractmethod
    def info(message: str = '') -> None:
        """
        Displays an informational message to the console.

        Parameters
        ----------
        message : str
            The message to display.
        """
        pass

    @staticmethod
    @abstractmethod
    def fail(message: str = '') -> None:
        """
        Displays a failure message to the console.

        Parameters
        ----------
        message : str
            The message to display.
        """
        pass

    @staticmethod
    @abstractmethod
    def error(message: str = '') -> None:
        """
        Displays an error message to the console and terminates the program.

        Parameters
        ----------
        message : str
            The message to display.
        """
        pass
