import os
from orionis.luminate.files.paths import SkeletonPath
from orionis.luminate.contracts.facades.paths_interface import IPath

class Path(IPath):

    @staticmethod
    def _resolve_directory(directory: str, file: str = None):
        """
        Internal helper function to resolve an absolute path for a given directory.

        Parameters
        ----------
        directory : str
            The base directory to resolve the path from.
        file : str, optional
            The relative file path inside the directory (default is an empty string).

        Returns
        -------
        SkeletonPath
            The resolved absolute path wrapped in a SkeletonPath object.
        """
        # Default to an empty string if None
        file = file or ""

        # Construct path safely
        route = os.path.join(directory, file)

        # Normalize path (removes redundant slashes)
        route = os.path.normpath(route)

        return SkeletonPath(route).resolve()

    @staticmethod
    def app(file: str = None):
        """
        Returns the absolute path for a file inside the 'app' directory.

        Parameters
        ----------
        file : str, optional
            The relative file path inside the 'app' directory.

        Returns
        -------
        SkeletonPath
            The resolved path wrapped in a SkeletonPath object.
        """
        return Path._resolve_directory("app", file)

    @staticmethod
    def config(file: str = None):
        """
        Returns the absolute path for a file inside the 'config' directory.

        Parameters
        ----------
        file : str, optional
            The relative file path inside the 'config' directory.

        Returns
        -------
        SkeletonPath
            The resolved path wrapped in a SkeletonPath object.
        """
        return Path._resolve_directory("config", file)

    @staticmethod
    def database(file: str = None):
        """
        Returns the absolute path for a file inside the 'database' directory.

        Parameters
        ----------
        file : str, optional
            The relative file path inside the 'database' directory.

        Returns
        -------
        SkeletonPath
            The resolved path wrapped in a SkeletonPath object.
        """
        return Path._resolve_directory("database", file)

    @staticmethod
    def resource(file: str = None):
        """
        Returns the absolute path for a file inside the 'resource' directory.

        Parameters
        ----------
        file : str, optional
            The relative file path inside the 'resource' directory.

        Returns
        -------
        SkeletonPath
            The resolved path wrapped in a SkeletonPath object.
        """
        return Path._resolve_directory("resource", file)

    @staticmethod
    def routes(file: str = None):
        """
        Returns the absolute path for a file inside the 'routes' directory.

        Parameters
        ----------
        file : str, optional
            The relative file path inside the 'routes' directory.

        Returns
        -------
        SkeletonPath
            The resolved path wrapped in a SkeletonPath object.
        """
        return Path._resolve_directory("routes", file)

    @staticmethod
    def storage(file: str = None):
        """
        Returns the absolute path for a file inside the 'storage' directory.

        Parameters
        ----------
        file : str, optional
            The relative file path inside the 'storage' directory.

        Returns
        -------
        SkeletonPath
            The resolved path wrapped in a SkeletonPath object.
        """
        return Path._resolve_directory("storage", file)

    @staticmethod
    def tests(file: str = None):
        """
        Returns the absolute path for a file inside the 'tests' directory.

        Parameters
        ----------
        file : str, optional
            The relative file path inside the 'tests' directory.

        Returns
        -------
        SkeletonPath
            The resolved path wrapped in a SkeletonPath object.
        """
        return Path._resolve_directory("tests", file)


# -------------- Functions --------------


def app_path(file: str = None):
    """
    Returns the absolute path for a file inside the 'app' directory.

    Parameters
    ----------
    file : str, optional
        The relative file path inside the 'app' directory.

    Returns
    -------
    SkeletonPath
        The resolved path wrapped in a SkeletonPath object.
    """
    return Path._resolve_directory("app", file)

def config_path(file: str = None):
    """
    Returns the absolute path for a file inside the 'config' directory.

    Parameters
    ----------
    file : str, optional
        The relative file path inside the 'config' directory.

    Returns
    -------
    SkeletonPath
        The resolved path wrapped in a SkeletonPath object.
    """
    return Path._resolve_directory("config", file)

def database_path(file: str = None):
    """
    Returns the absolute path for a file inside the 'database' directory.

    Parameters
    ----------
    file : str, optional
        The relative file path inside the 'database' directory.

    Returns
    -------
    SkeletonPath
        The resolved path wrapped in a SkeletonPath object.
    """
    return Path._resolve_directory("database", file)

def resource_path(file: str = None):
    """
    Returns the absolute path for a file inside the 'resource' directory.

    Parameters
    ----------
    file : str, optional
        The relative file path inside the 'resource' directory.

    Returns
    -------
    SkeletonPath
        The resolved path wrapped in a SkeletonPath object.
    """
    return Path._resolve_directory("resource", file)

def routes_path(file: str = None):
    """
    Returns the absolute path for a file inside the 'routes' directory.

    Parameters
    ----------
    file : str, optional
        The relative file path inside the 'routes' directory.

    Returns
    -------
    SkeletonPath
        The resolved path wrapped in a SkeletonPath object.
    """
    return Path._resolve_directory("routes", file)

def storage_path(file: str = None):
    """
    Returns the absolute path for a file inside the 'storage' directory.

    Parameters
    ----------
    file : str, optional
        The relative file path inside the 'storage' directory.

    Returns
    -------
    SkeletonPath
        The resolved path wrapped in a SkeletonPath object.
    """
    return Path._resolve_directory("storage", file)

def tests_path(file: str = None):
    """
    Returns the absolute path for a file inside the 'tests' directory.

    Parameters
    ----------
    file : str, optional
        The relative file path inside the 'tests' directory.

    Returns
    -------
    SkeletonPath
        The resolved path wrapped in a SkeletonPath object.
    """
    return Path._resolve_directory("tests", file)
