from abc import ABC, abstractmethod

class IOutput(ABC):
    """
    Interface for console display operations.

    Defines methods for displaying different types of messages, such as informational,
    success, failure, and error messages.
    """

    @abstractmethod
    def welcome(self):
        """
        Displays a welcome message to the framework.

        This method does not take any parameters and does not return any value.
        """
        pass

    @abstractmethod
    def finished(self):
        """
        Displays a message indicating the completion of the process.

        This method does not take any parameters and does not return any value.
        """
        pass

    @abstractmethod
    def info(self, message: str):
        """
        Displays an informational message.

        Parameters
        ----------
        message : str
            The message to display. It is displayed with an informational prefix and timestamp.

        Returns
        -------
        None
        """
        pass

    @abstractmethod
    def fail(self, message: str):
        """
        Displays a failure message.

        Parameters
        ----------
        message : str
            The message to display. It is displayed with a failure prefix and timestamp.

        Returns
        -------
        None
        """
        pass

    @abstractmethod
    def error(self, message: str):
        """
        Displays an error message and terminates the program.

        Parameters
        ----------
        message : str
            The error message to display. It is displayed with an error prefix and timestamp.

        Returns
        -------
        None

        Raises
        ------
        SystemExit
            Exits the program with an error code (1).
        """
        pass
