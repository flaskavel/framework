from abc import ABC, abstractmethod

class IPath(ABC):

    @abstractmethod
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
        pass

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