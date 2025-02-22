from abc import ABC, abstractmethod
from typing import Optional

class ILogguerService(ABC):

    @abstractmethod
    def _initialize_logger(self, path: Optional[str], level: int, filename: Optional[str] = 'orionis.log'):
        """
        Configures the logger with the specified settings.

        This method sets up the logger to write logs to a file. If the specified
        directory does not exist, it creates it. The log format includes the
        timestamp and the log message.

        Parameters
        ----------
        path : Optional[str]
            The directory path where the log file will be stored.
        level : int
            The logging level (e.g., logging.INFO, logging.ERROR).
        filename : Optional[str]
            The name of the log file.

        Raises
        ------
        RuntimeError
            If the logger cannot be initialized due to an error.
        """
        pass

    @abstractmethod
    def info(self, message: str) -> None:
        """
        Logs an informational message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """
        Logs an error message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        pass

    @abstractmethod
    def success(self, message: str) -> None:
        """
        Logs a success message (treated as info).

        Parameters
        ----------
        message : str
            The message to log.
        """
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """
        Logs a warning message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        """
        Logs a debug message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        pass