from abc import ABC, abstractmethod

class ILogger(ABC):
    """
    Abstract base class for a logger.

    This defines the contract that any concrete logger class must implement.
    """

    @abstractmethod
    def info(self, message: str) -> None:
        """Logs an informational message."""
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Logs an error message."""
        pass

    @abstractmethod
    def success(self, message: str) -> None:
        """Logs a success message (treated as info)."""
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """Logs a warning message."""
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        """Logs a debug message."""
        pass