from abc import ABC, abstractmethod

class IInstallerOutput(ABC):
    """
    Interface for the InstallerOutput class.
    """

    @abstractmethod
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
        pass

    @abstractmethod
    def asciiIco():
        """
        Displays a welcome message to the framework, including ASCII art.

        Attempts to load an ASCII art file (art.ascii). If not found, defaults to displaying basic information.

        If the ASCII art file is found, placeholders are replaced with dynamic content such as version, docs, and year.
        """
        pass

    @abstractmethod
    def asciiInfo():
        """
        Displays another type of welcome message to the framework, including different ASCII art.

        Attempts to load an ASCII art file (info.ascii). If not found, defaults to displaying basic information.

        Similar to `asciiIco()`, but with different ASCII art.
        """
        pass

    @abstractmethod
    def startInstallation():
        """
        Displays the starting message when the installation begins.
        This includes a welcoming message and the ASCII art.
        """
        pass

    @abstractmethod
    def endInstallation():
        """
        Displays the ending message after the installation is complete.
        Provides a message of encouragement to start using the framework.
        """
        pass

    @abstractmethod
    def info(message: str = ''):
        """
        Displays an informational message to the console.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.
        """
        pass

    @abstractmethod
    def fail(message: str = ''):
        """
        Displays a failure message to the console.

        Parameters
        ----------
        message : str, optional
            The message to display. Defaults to an empty string.
        """
        pass

    @abstractmethod
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
        pass