import os
import threading

class _Paths:
    """
    Singleton class that manages directory paths. Ensures only one instance
    of the path management logic is created, using a thread-safe implementation.
    """

    # Class-level variable to store the singleton instance
    _instance = None

    # Thread lock for thread-safe singleton initialization
    _lock = threading.Lock()

    def __new__(cls, path: str = None):
        """
        Creates a new instance of the _Paths class if it does not already exist.
        Ensures thread safety using a lock to prevent race conditions.

        :param path: Optional string to specify the base directory. If not provided, a default path is used.
        :return: The singleton instance of the _Paths class.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(_Paths, cls).__new__(cls)
                cls._instance._initialize(path)
        return cls._instance

    def _initialize(self, path: str = None):
        """
        Initializes the instance with a base directory. If no directory is provided, a default one is set.

        :param path: Optional string to specify the base directory.
        """
        # Use provided directory or set default based on the current file's location
        self.path = path if path else os.path.abspath(os.path.join(__file__, '../../../../../../../'))

    def get_directory(self, path: str = None) -> str:
        """
        Returns the absolute path for a given relative directory based on the base path.
        Ensures that the requested path is a directory.

        :param path: The relative directory to be resolved against the base path.
        :return: The absolute directory path if it exists.
        :raises: ValueError if the path does not exist or is not a directory.
        """
        # Combine base path with the provided relative directory
        real_path = os.path.join(self.path, path)

        # Check if the resolved path exists and is a directory
        if os.path.isdir(real_path):
            return os.path.abspath(real_path)

        # Raise an exception if the directory does not exist or is not a directory
        raise ValueError(f"The requested directory does not exist or is not a directory: {real_path}")