from flaskavel.lab.catalyst.logger import Logguer

class Log:
    """A logging utility class that provides static methods for logging at various levels."""

    @staticmethod
    def info(message: str):
        """Logs an informational message."""
        # Get the singleton logger instance.
        instance = Logguer()

        # Log the message as info.
        instance.info(message=message)

    @staticmethod
    def error(message: str):
        """Logs an error message."""
        # Get the singleton logger instance.
        instance = Logguer()

        # Log the message as an error.
        instance.error(message=message)

    @staticmethod
    def success(message: str):
        """Logs a success message (treated as an info level log)."""
        # Get the singleton logger instance.
        instance = Logguer()

        # Log the message as success.
        instance.success(message=message)

    @staticmethod
    def warning(message: str):
        """Logs a warning message."""
        # Get the singleton logger instance.
        instance = Logguer()

        # Log the message as a warning.
        instance.warning(message=message)
