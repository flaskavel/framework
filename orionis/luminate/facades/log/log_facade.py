from orionis.contracts.facades.log.i_log_facade import ILog
from orionis.luminate.app_context import AppContext
from orionis.luminate.services.log.log_service import LogguerService

class Log(ILog):
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

    @staticmethod
    def info(message: str) -> None:
        """
        Logs an informational message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        LogguerService().info(message)

    @staticmethod
    def error(message: str) -> None:
        """
        Logs an error message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        LogguerService().error(message)

    @staticmethod
    def success(message: str) -> None:
        """
        Logs a success message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        LogguerService().success(message)

    @staticmethod
    def warning(message: str) -> None:
        """
        Logs a warning message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        LogguerService().warning(message)

    @staticmethod
    def debug(message: str) -> None:
        """
        Logs a debug message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        LogguerService().debug(message)