
import subprocess
import sys
from orionis.contracts.installer.i_installer_manager import IInstallerManager
from orionis.installer.installer_output import InstallerOutput
from orionis.installer.installer_setup import InstallerSetup

class InstallerManager(IInstallerManager):
    """
    Management class responsible for handling framework-related operations.

    This class provides methods to display the framework version, execute upgrades,
    create new applications, and display additional information.

    Attributes
    ----------
    output : InstallerOutput
        Instance of Output to manage command-line display messages.
    """

    def __init__(self, output = InstallerOutput):
        """
        Initialize the Management class with an output handler.

        Parameters
        ----------
        output : Output
            An instance of Output to handle command-line messages.
        """
        self.output = output

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
        try:
            return self.output.asciiIco()
        except Exception as e:
            raise RuntimeError(f"Failed to display version: {e}")

    def handleUpgrade(self) -> None:
        """
        Execute the framework upgrade process to the latest version.

        Raises
        ------
        Exception
            If an error occurs during the upgrade process.
        """
        try:
            self.output.info("Starting the upgrade process...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "orionis"])
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Upgrade failed: {e}")
        except Exception as e:
            raise RuntimeError(f"Upgrade failed: {e}")


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
        try:
            InstallerSetup(name=name_app, output=self.output).handle()
        except Exception as e:
            raise RuntimeError(f"Failed to create new app: {e}")

    def handleInfo(self) -> None:
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