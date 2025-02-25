from abc import ABC, abstractmethod

class IPath(ABC):
    """
    A facade class for resolving absolute paths to various application directories.

    This class provides static methods to resolve paths to common directories such as
    'app', 'config', 'database', 'resources', 'routes', 'storage', and 'tests'.
    It uses the `PathService` to resolve and validate paths.

    Methods
    -------
    _resolve_directory(directory: str, file: str = None) -> SkeletonPath
        Resolves the absolute path for a given directory and optional file.
    app(file: str = None) -> SkeletonPath
        Returns the absolute path for a file inside the 'app' directory.
    config(file: str = None) -> SkeletonPath
        Returns the absolute path for a file inside the 'config' directory.
    database(file: str = None) -> SkeletonPath
        Returns the absolute path for a file inside the 'database' directory.
    resource(file: str = None) -> SkeletonPath
        Returns the absolute path for a file inside the 'resource' directory.
    routes(file: str = None) -> SkeletonPath
        Returns the absolute path for a file inside the 'routes' directory.
    storage(file: str = None) -> SkeletonPath
        Returns the absolute path for a file inside the 'storage' directory.
    tests(file: str = None) -> SkeletonPath
        Returns the absolute path for a file inside the 'tests' directory.
    """

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
