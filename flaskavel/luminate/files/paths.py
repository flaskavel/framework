import os
from pathlib import Path as SysPath
from flaskavel.luminate.contracts.files.paths_interface import ISkeletonPath

class SkeletonPath(ISkeletonPath):
    """
    Resolves the absolute path for a given relative directory based on the script's execution directory.
    Ensures that the requested path is a valid directory.

    Attributes
    ----------
    route : str
        The resolved absolute path to the directory.

    Methods
    -------
    __str__():
        Returns the absolute path as a string.
    """

    def __init__(self, route: str):
        """
        Initializes the Path class, resolving the absolute path for a given relative directory.

        The path is resolved relative to the script's execution directory.

        Parameters
        ----------
        route : str
            The relative directory path to be resolved.

        Raises
        ------
        ValueError
            If the path does not exist or is not a directory.
        """
        # Get the absolute path based on the script's execution directory
        base_path = SysPath(os.getcwd())  # Get the directory where the script is executed
        real_path = (base_path / route).resolve()  # Combine base path with the relative route

        # Validate that the path exists and is a directory
        if not real_path.is_dir():
            raise ValueError(f"The requested directory does not exist or is not a directory: {real_path}")

        self.route = str(real_path)

    def resolve(self) -> str:
        """
        Returns the absolute path as a string.

        Returns
        -------
        str
            The absolute directory path.
        """
        return self.route
