from abc import ABC, abstractmethod

class IPypiPublisher(ABC):
    """
    Interface for managing the publishing process of a package to PyPI
    and handling repository operations.
    """

    @abstractmethod
    def gitPush(self):
        """
        Commits and pushes changes to the Git repository if modifications are detected.
        """
        pass

    @abstractmethod
    def publish(self):
        """
        Uploads the package to PyPI using Twine.

        The PyPI token should be retrieved from the environment variable or
        passed during initialization.
        """
        pass

    @abstractmethod
    def clearRepository(self):
        """
        Deletes temporary directories created during the publishing process.

        The following directories should be removed:
        - build
        - dist
        - flaskavel.egg-info
        """
        pass
