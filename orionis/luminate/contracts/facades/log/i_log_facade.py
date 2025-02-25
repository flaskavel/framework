from abc import ABC, abstractmethod

class ILog(ABC):
    """
    A facade class for logging messages with different severity levels.

    This class provides static methods to log messages using the `LogguerService`.
    It simplifies the process of logging by abstracting the service resolution
    and providing a clean interface for logging.

    Methods
    -------
    info(message: str) -> None
        Logs an informational message.
    error(message: str) -> None
        Logs an error message.
    success(message: str) -> None
        Logs a success message.
    warning(message: str) -> None
        Logs a warning message.
    debug(message: str) -> None
        Logs a debug message.
    """

    @abstractmethod
    def info(message: str) -> None:
        """
        Logs an informational message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        pass

    @abstractmethod
    def error(message: str) -> None:
        """
        Logs an error message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        pass

    @abstractmethod
    def success(message: str) -> None:
        """
        Logs a success message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        pass

    @abstractmethod
    def warning(message: str) -> None:
        """
        Logs a warning message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        pass

    @abstractmethod
    def debug(message: str) -> None:
        """
        Logs a debug message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        pass