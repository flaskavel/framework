from orionis.luminate.installer.setup import Setup
from orionis.luminate.installer.output import Output
from orionis.luminate.installer.upgrade import Upgrade
from orionis.luminate.contracts.console.management_interface import IManagement

class Management(IManagement):
    """
    Management class responsible for handling framework-related operations.

    This class provides methods to display the framework version, execute upgrades,
    create new applications, and display additional information.

    Attributes
    ----------
    output : Output
        Instance of Output to manage command-line display messages.
    """

    def __init__(self, output = Output):
        """
        Initialize the Management class with an output handler.

        Parameters
        ----------
        output : Output
            An instance of Output to handle command-line messages.
        """
        self.output = output

    def displayVersion(self) -> str:
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
        try:
            return self.output.asciiIco()
        except Exception as e:
            raise RuntimeError(f"Failed to display version: {e}")

    def executeUpgrade(self) -> None:
        """
        Execute the framework upgrade process to the latest version.

        Raises
        ------
        Exception
            If an error occurs during the upgrade process.
        """
        try:
            Upgrade.execute()
        except Exception as e:
            raise RuntimeError(f"Upgrade process failed: {e}")

    def createNewApp(self, name_app: str = "example-app") -> None:
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
        try:
            Setup(name_app).handle()
        except Exception as e:
            raise RuntimeError(f"Failed to create application '{name_app}': {e}")

    def displayInfo(self) -> None:
        """
        Display additional framework information in ASCII format.

        Raises
        ------
        Exception
            If an error occurs while displaying information.
        """
        try:
            self.output.asciiInfo()
        except Exception as e:
            raise RuntimeError(f"Failed to display information: {e}")
