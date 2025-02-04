from abc import ABC, abstractmethod

class IManagement(ABC):
    """
    Interface defining the contract for the Management class.

    This interface ensures that any implementing class provides methods for 
    displaying the framework version, upgrading the framework, creating a new 
    application, and displaying additional information.
    """

    @abstractmethod
    def displayVersion(self) -> str:
        """
        Display the current version of the framework.

        Returns
        -------
        str
            The ASCII representation of the framework version.
        """
        pass

    @abstractmethod
    def executeUpgrade(self) -> None:
        """
        Execute the framework upgrade process to the latest version.

        Raises
        ------
        Exception
            If an error occurs during the upgrade process.
        """
        pass

    @abstractmethod
    def createNewApp(self, name_app: str) -> None:
        """
        Create a new application with the given name.

        Parameters
        ----------
        name_app : str
            The name of the new application.

        Raises
        ------
        Exception
            If an error occurs during the application setup.
        """
        pass

    @abstractmethod
    def displayInfo(self) -> None:
        """
        Display additional information about the framework.

        Raises
        ------
        Exception
            If an error occurs while displaying information.
        """
        pass
