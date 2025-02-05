import logging
from typing import Optional
from flaskavel.luminate.log.logger import Logguer
from flaskavel.luminate.contracts.log.logger_interface import ILogger

class Log:
    """
    Facade for accessing the Logguer instance.

    Provides a simplified interface for logging messages.
    """

    @staticmethod
    def info(message: str) -> None:
        """Logs an informational message."""
        Logguer().info(message)

    @staticmethod
    def error(message: str) -> None:
        """Logs an error message."""
        Logguer().error(message)

    @staticmethod
    def success(message: str) -> None:
        """Logs a success message (treated as info)."""
        Logguer().success(message)

    @staticmethod
    def warning(message: str) -> None:
        """Logs a warning message."""
        Logguer().warning(message)

    @staticmethod
    def debug(message: str) -> None:
        """Logs a debug message."""
        Logguer().debug(message)

    @staticmethod
    def configure(path: Optional[str] = None, level: int = logging.INFO) -> ILogger:
        """
        Configures and returns the Logguer instance.

        Parameters
        ----------
        path : str, optional
            The file path where logs will be stored. If None, a default path is used.
        level : int, optional
            The logging level (default is logging.INFO).

        Returns
        -------
        ILogger
            Configured logger instance.
        """
        return Logguer(path, level)
