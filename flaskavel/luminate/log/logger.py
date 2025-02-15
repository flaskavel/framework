import os
import logging
import threading
from pathlib import Path
from typing import Optional
from flaskavel.luminate.contracts.log.logger_interface import ILogger

class Logguer(ILogger):
    """
    A thread-safe singleton logger class for logging messages.

    Attributes
    ----------
    logger : logging.Logger
        The logger instance used for logging messages.

    Methods
    -------
    info(message: str)
        Logs an informational message.
    error(message: str)
        Logs an error message.
    success(message: str)
        Logs a success message (treated as info).
    warning(message: str)
        Logs a warning message.
    debug(message: str)
        Logs a debug message.
    """

    # Singleton instance
    _instance = None

    # Thread-safe instance creation
    _lock = threading.Lock()

    def __new__(cls, path: Optional[str] = None, level: int = logging.INFO, filename: Optional[str] = 'flaskavel.log'):
        """
        Creates or returns the singleton instance of the Logguer class.

        Parameters
        ----------
        path : str, optional
            The file path where logs will be stored. If None, a default path is used.
        level : int, optional
            The logging level (default is logging.INFO).

        Returns
        -------
        Logguer
            The singleton instance of the logger.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Logguer, cls).__new__(cls)
                cls._instance._initialize_logger(path, level, filename)
        return cls._instance

    def _initialize_logger(self, path: Optional[str], level: int, filename: Optional[str] = 'flaskavel.log'):
        """
        Initializes the logger with the specified log file path and logging level.

        Parameters
        ----------
        path : str, optional
            The file path where logs will be stored.
        level : int
            The logging level.
        """
        try:

            if path is None:
                base_path = Path(os.getcwd())
                log_dir = base_path / "storage" / "logs"

                # Check if the log directory exists
                if log_dir.exists():
                    path = log_dir / filename
                else:
                    path = base_path / filename

            logging.basicConfig(
                level=level,
                format="%(asctime)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                encoding="utf-8",
                handlers=[
                    logging.FileHandler(path)
                    # logging.StreamHandler()
                ]
            )

            self.logger = logging.getLogger(__name__)

        except Exception as e:
            raise RuntimeError(f"Failed to initialize logger: {e}")

    def info(self, message: str) -> None:
        """Logs an informational message."""
        self.logger.info(f"[INFO] - {message}")

    def error(self, message: str) -> None:
        """Logs an error message."""
        self.logger.error(f"[ERROR] - {message}")

    def success(self, message: str) -> None:
        """Logs a success message (treated as info)."""
        self.logger.info(f"[SUCCESS] - {message}")

    def warning(self, message: str) -> None:
        """Logs a warning message."""
        self.logger.warning(f"[WARNING] - {message}")

    def debug(self, message: str) -> None:
        """Logs a debug message."""
        self.logger.debug(f"[DEBUG] - {message}")
