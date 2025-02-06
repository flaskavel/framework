from abc import ABC, abstractmethod
from typing import Optional
import logging
from flaskavel.luminate.contracts.log.logger_interface import ILogger

class ILogFacade(ABC):
    """
    Facade interface for simplified access to logging operations.

    Methods
    -------
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
    configure(path: Optional[str], level: int) -> ILogger
        Configures and returns the logger instance.
    """

    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        pass

    @abstractmethod
    def success(self, message: str) -> None:
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        pass

    @abstractmethod
    def configure(self, path: Optional[str] = None, level: int = logging.INFO) -> ILogger:
        pass
