import os
import logging
import threading

class Logguer:
    """A singleton logger class that provides various logging methods."""

    _instance = None  # Holds the single instance of the Logguer class.
    _lock = threading.Lock()  # Ensures thread-safe access to the logger instance.

    def __new__(cls, path: str = None):
        """Creates a new instance of the Logguer class or returns the existing instance."""
        with cls._lock:
            if cls._instance is None:  # Check if an instance already exists.
                cls._instance = super(Logguer, cls).__new__(cls)
                cls._instance._initialize_logger(path)  # Initialize the logger.
        return cls._instance  # Return the singleton instance.

    def _initialize_logger(self, path: str = None):
        """Initializes the logger with the specified log file path or a default path."""

        if not path:  # If no path is provided, set a default path.
            path_log_dir = os.path.abspath(os.path.join(__file__, '../../../../../../../storage/logs'))
            os.makedirs(path_log_dir, exist_ok=True)  # Create the log directory if it doesn't exist.
            path_log = os.path.join(path_log_dir, 'flaskavel.log')  # Default log file name.
            path = path_log  # Use the default path.

        logging.basicConfig(
            level=logging.INFO,  # Set the logging level to INFO.
            format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log message format.
            datefmt='%Y-%m-%d %H:%M:%S',  # Set the date format for log entries.
            encoding='utf-8',  # Set the encoding for the log file.
            handlers=[  # Define the handlers for logging.
                logging.FileHandler(path),  # Log to the specified file.
            ]
        )
        self.logger = logging.getLogger()  # Get the logger instance.

    def info(self, message: str):
        """Logs an informational message."""
        self.logger.info(message)

    def error(self, message: str):
        """Logs an error message."""
        self.logger.error(message)

    def success(self, message: str):
        """Logs a success message (treated as an info level log)."""
        self.logger.info(message)

    def warning(self, message: str):
        """Logs a warning message."""
        self.logger.warning(message)

    def debug(self, message: str):
        """Logs a debug message."""
        self.logger.debug(message)
