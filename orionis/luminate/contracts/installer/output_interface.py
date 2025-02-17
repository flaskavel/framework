from abc import ABC, abstractmethod

class IOutput(ABC):
    """
    Interface defining the contract for the Output class.

    This interface ensures that any implementing class provides methods for
    displaying messages, ASCII-based framework information, and handling errors.

    Methods
    -------
    asciiIco() -> None
        Displays the framework's ASCII icon along with relevant information.
    asciiInfo() -> None
        Displays additional ASCII-based information about the framework.
    startInstallation() -> None
        Shows a welcome message when installation starts.
    endInstallation() -> None
        Shows a completion message when installation finishes.
    info(message: str) -> None
        Displays an informational message.
    fail(message: str) -> None
        Displays a failure message.
    error(message: str) -> None
        Displays an error message and terminates the program.
    """

    @abstractmethod
    def asciiIco(self) -> None:
        """
        Displays the framework's ASCII icon along with relevant information.

        Raises
        ------
        Exception
            If an error occurs while displaying the ASCII art.
        """
        pass

    @abstractmethod
    def asciiInfo(self) -> None:
        """
        Displays additional ASCII-based information about the framework.

        Raises
        ------
        Exception
            If an error occurs while displaying the ASCII information.
        """
        pass

    @abstractmethod
    def startInstallation(self) -> None:
        """
        Shows a welcome message when installation starts.

        Raises
        ------
        Exception
            If an error occurs during message display.
        """
        pass

    @abstractmethod
    def endInstallation(self) -> None:
        """
        Shows a completion message when installation finishes.

        Raises
        ------
        Exception
            If an error occurs during message display.
        """
        pass

    @abstractmethod
    def info(self, message: str) -> None:
        """
        Displays an informational message.

        Parameters
        ----------
        message : str
            The message to display.

        Raises
        ------
        Exception
            If an error occurs while displaying the message.
        """
        pass

    @abstractmethod
    def fail(self, message: str) -> None:
        """
        Displays a failure message.

        Parameters
        ----------
        message : str
            The message to display.

        Raises
        ------
        Exception
            If an error occurs while displaying the message.
        """
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """
        Displays an error message and terminates the program.

        Parameters
        ----------
        message : str
            The message to display.

        Raises
        ------
        SystemExit
            Terminates the program with an exit code.
        """
        pass
