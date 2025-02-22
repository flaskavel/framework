
from abc import ABC, abstractmethod

class IInstallerManager(ABC):
    """
    Interface for the InstallerManager class.
    """

    @abstractmethod
    def handleVersion(self) -> str:
        """
        Display the current version of the framework in ASCII format.

        Returns
        -------
        str
            The ASCII representation of the framework version.

        Raises
        ------
        Exception
            If an error occurs while generating the ASCII version output.
        """
        pass

    @abstractmethod
    def handleUpgrade(self) -> None:
        """
        Execute the framework upgrade process to the latest version.

        Raises
        ------
        Exception
            If an error occurs during the upgrade process.
        """
        pass


    @abstractmethod
    def handleNewApp(self, name_app: str = "example-app") -> None:
        """
        Create a new application with the specified name.

        Parameters
        ----------
        name_app : str, optional
            The name of the new application (default is "example-app").

        Raises
        ------
        Exception
            If an error occurs during the application setup.
        """
        pass

    @abstractmethod
    def handleInfo(self) -> None:
        """
        Display additional framework information in ASCII format.

        Raises
        ------
        Exception
            If an error occurs while displaying information.
        """
        pass