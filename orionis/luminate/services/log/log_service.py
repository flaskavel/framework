import os
import logging
from pathlib import Path
from typing import Optional
from orionis.contracts.services.log.i_log_service import ILogguerService

class LogguerService(ILogguerService):
    """
    A service class for logging messages with different severity levels.

    This class initializes a logger that can write logs to a file. It supports
    various log levels such as INFO, ERROR, SUCCESS, WARNING, and DEBUG.

    Attributes
    ----------
    logger : logging.Logger
        The logger instance used to log messages.

    Methods
    -------
    __init__(path: Optional[str] = None, level: int = logging.INFO, filename: Optional[str] = 'orionis.log')
        Initializes the logger with the specified path, log level, and filename.
    _initialize_logger(path: Optional[str], level: int, filename: Optional[str] = 'orionis.log')
        Configures the logger with the specified settings.
    info(message: str) -> None
        Logs an informational message.
    error(message: str) -> None
        Logs an error message.
    success(message: str) -> None
        Logs a success message (treated as info).
    warning(message: str) -> None
        Logs a warning message.
    debug(message: str) -> None
        Logs a debug message.
    """

    def __init__(self, path: Optional[str] = None, level: int = logging.INFO, filename: Optional[str] = 'orionis.log'):
        """
        Initializes the logger with the specified path, log level, and filename.

        Parameters
        ----------
        path : Optional[str]
            The directory path where the log file will be stored. If not provided,
            it defaults to a 'logs' directory inside the 'storage' folder of the
            current working directory.
        level : int
            The logging level (e.g., logging.INFO, logging.ERROR). Defaults to logging.INFO.
        filename : Optional[str]
            The name of the log file. Defaults to 'orionis.log'.
        """
        self._initialize_logger(path, level, filename)

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
        try:
            # Resolve the log directory and file path
            if path is None:
                base_path = Path(os.getcwd())
                log_dir = base_path / "storage" / "logs"

                # Create the log directory if it does not exist
                if not log_dir.exists():
                    log_dir.mkdir(parents=True, exist_ok=True)

                path = log_dir / filename

            # Configure the logger
            logging.basicConfig(
                level=level,
                format="%(asctime)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                encoding="utf-8",
                handlers=[
                    logging.FileHandler(path)  # Log to a file
                    # logging.StreamHandler()  # Uncomment to also log to the console
                ]
            )

            # Get the logger instance
            self.logger = logging.getLogger(__name__)

        except Exception as e:
            raise RuntimeError(f"Failed to initialize logger: {e}")

    def info(self, message: str) -> None:
        """
        Logs an informational message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        self.logger.info(f"[INFO] - {message}")

    def error(self, message: str) -> None:
        """
        Logs an error message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        self.logger.error(f"[ERROR] - {message}")

    def success(self, message: str) -> None:
        """
        Logs a success message (treated as info).

        Parameters
        ----------
        message : str
            The message to log.
        """
        self.logger.info(f"[SUCCESS] - {message}")

    def warning(self, message: str) -> None:
        """
        Logs a warning message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        self.logger.warning(f"[WARNING] - {message}")

    def debug(self, message: str) -> None:
        """
        Logs a debug message.

        Parameters
        ----------
        message : str
            The message to log.
        """
        self.logger.debug(f"[DEBUG] - {message}")