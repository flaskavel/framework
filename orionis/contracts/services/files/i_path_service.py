import os
from pathlib import Path
from abc import ABC, abstractmethod

class IPathService(ABC):

    @abstractmethod
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
        ValueError
            If the resolved path does not exist or is neither a directory nor a file.
        """
        pass