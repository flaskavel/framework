from flaskavel.lab.catalyst.logger import Logguer

class Log:
    """A logging utility class that provides static methods for logging at various levels."""

    @staticmethod
    def info(message: str):
        """Logs an informational message."""
        instance = Logguer()  # Get the singleton logger instance.
        instance.info(message=message)  # Log the message as info.

    @staticmethod
    def error(message: str):
        """Logs an error message."""
        instance = Logguer()  # Get the singleton logger instance.
        instance.error(message=message)  # Log the message as an error.

    @staticmethod
    def success(message: str):
        """Logs a success message (treated as an info level log)."""
        instance = Logguer()  # Get the singleton logger instance.
        instance.success(message=message)  # Log the message as success.

    @staticmethod
    def warning(message: str):
        """Logs a warning message."""
        instance = Logguer()  # Get the singleton logger instance.
        instance.warning(message=message)  # Log the message as a warning.
