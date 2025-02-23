import logging
import os
import re
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from orionis.contracts.services.log.i_log_service import ILogguerService
from orionis.luminate.services.config.config_service import ConfigService

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
    __init__(config_service: ConfigService)
        Initializes the logger with ConfigService
    _initialize_logger(config_service: ConfigService)
        Configures the logger with ConfigService settings.
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

    def __init__(self, config_service : ConfigService):
        """
        Initializes the logger with the specified path, log level, and filename.

        Parameters
        ----------
        config_service : ConfigService
            The configuration service instance.
        """
        self.config_service = config_service
        self._initialize_logger()

    def _initialize_logger(self):
        """
        Configures the logger with the specified settings.

        This method sets up the logger to write logs to a file. If the specified
        directory does not exist, it creates it. The log format includes the
        timestamp and the log message.

        Parameters
        ----------
        config_service : ConfigService
            The configuration service instance.

        Raises
        ------
        RuntimeError
            If the logger cannot be initialized due to an error.
        """
        try:

            handlers = []

            channel : str = self.config_service.get("logging.default")
            config : dict = self.config_service.get(f"logging.channels.{channel}", {})
            path : str = config.get("path", 'logs/orionis.log')
            app_timezone : str = self.config_service.get("app.timezone", "UTC")

            if channel == "stack":

                handlers = [
                    logging.FileHandler(
                        filename=path,
                        encoding="utf-8"
                    )
                ]

            elif channel == "hourly":

                handlers = [
                    TimedRotatingFileHandler(
                        filename=path,
                        when="h",
                        interval=1,
                        backupCount=config.get('retention_hours', 24),
                        encoding="utf-8",
                        utc= True if app_timezone == "UTC" else False
                    )
                ]

            elif channel == "daily":

                backup_count = config.get('retention_days', 30)
                hour_at:str = config.get('at', "00:00")
                if backup_count < 1:
                    raise ValueError("The 'retention_days' value must be an integer greater than 0.")
                if not bool(re.match(r"^(?:[01]?\d|2[0-3]):[0-5]?\d$", hour_at)):
                    raise ValueError("The 'at' value must be a valid time in the format HH:MM.")

                handlers = [
                    TimedRotatingFileHandler(
                        filename=path,
                        when="d",
                        interval=1,
                        backupCount=backup_count,
                        encoding="utf-8",
                        atTime=datetime.strptime(hour_at, "%H:%M").time(),
                        utc= True if app_timezone == "UTC" else False
                    )
                ]

            elif channel == "weekly":

                backup_count = config.get('retention_weeks', 4)
                if backup_count < 1:
                    raise ValueError("The 'retention_weeks' value must be an integer greater than 0.")
                handlers = [
                    TimedRotatingFileHandler(
                        filename=path,
                        when="w0",
                        interval=1,
                        backupCount=backup_count,
                        encoding="utf-8",
                        utc= True if app_timezone == "UTC" else False
                    )
                ]

            elif channel == "monthly":

                backup_count = config.get('retention_months', 2)
                if backup_count < 1:
                    raise ValueError("The 'retention_months' value must be an integer greater than 0.")
                handlers = [
                    TimedRotatingFileHandler(
                        filename=path,
                        when="midnight",
                        interval=30,
                        backupCount=backup_count,
                        encoding="utf-8",
                        utc= True if app_timezone == "UTC" else False
                    )
                ]

            elif channel == "chunked":

                max_bytes = config.get('mb_size', 5)
                if max_bytes < 1:
                    raise ValueError("The 'mb_size' value must be an integer greater than 0.")
                backup_count = config.get('max_files', 5)
                if backup_count < 1:
                    raise ValueError("The 'max_files' value must be an integer greater than 0.")
                handlers = [
                    RotatingFileHandler(
                        filename=path,
                        maxBytes= max_bytes * 1024 * 1024,
                        backupCount=backup_count,
                        encoding="utf-8"
                    )
                ]


            # Configure the logger
            logging.basicConfig(
                level=config.get("level", "INFO").upper(),
                format="%(asctime)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                encoding="utf-8",
                handlers=handlers
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