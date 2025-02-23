import os
import threading
from pathlib import Path
from orionis.contracts.services.files.i_path_resolver_service import IPathResolverService

class PathResolverService(IPathResolverService):

    _lock = threading.Lock()
    _instance = None

    def __new__(cls):
        """
        Override the __new__ method to ensure only one instance of the class is created.

        Returns
        -------
        PathResolverService
            The singleton instance of the PathResolverService class.
        """
        # Use the lock to ensure thread-safe instantiation
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.base_path = Path(os.getcwd())
        return cls._instance

    def resolve(self, route: str) -> str:
        """
        Resolves and returns the absolute path as a string.

        This method combines the base path (current working directory) with the provided
        relative path, resolves it to an absolute path, and validates that it exists
        and is either a directory or a file.

        Parameters
        ----------
        route : str
            The relative directory or file path to be resolved.

        Returns
        -------
        str
            The absolute path to the directory or file.

        Raises
        ------
        PathNotFoundError
            If the resolved path does not exist or is neither a directory nor a file.
        """
        # Combine base path with the relative route
        real_path = (self.base_path / route).resolve()

        # Validate that the path exists and is either a directory or a file
        if not real_path.exists():
            raise Exception(f"The requested path does not exist or is invalid: {real_path}")
        if not (real_path.is_dir() or real_path.is_file()):
            raise Exception(f"The requested path does not exist or is invalid: {real_path}")

        return str(real_path)
