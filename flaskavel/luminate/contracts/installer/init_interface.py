from abc import ABC, abstractmethod

class IInit(ABC):
    """
    Interface for the Init class to ensure consistency in handling initialization, upgrading, and application creation.

    Methods
    -------
    displayVersion() -> None
        Displays the current version of the Framework, including ASCII art.

    executeUpgrade() -> None
        Executes the upgrade process to the latest version of the Framework.

    createNewApp(name_app: str = 'example-app') -> None
        Creates a new application with the specified name.

    displayInfo() -> None
        Displays additional information, including ASCII art.
    """

    @abstractmethod
    def displayVersion(self) -> None:
        """
        Displays the current version of the Framework using ASCII art.
        """
        pass

    @abstractmethod
    def executeUpgrade(self) -> None:
        """
        Executes the upgrade process to the most recent version of the Framework.
        """
        pass

    @abstractmethod
    def createNewApp(self, name_app: str = 'example-app') -> None:
        """
        Creates a new application with the provided name.

        Parameters
        ----------
        name_app : str, optional
            The name of the new application (defaults to 'example-app').
        """
        pass

    @abstractmethod
    def displayInfo(self) -> None:
        """
        Displays additional information, including ASCII art.
        """
        pass
