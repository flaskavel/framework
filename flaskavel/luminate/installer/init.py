from flaskavel.luminate.contracts.installer.init_interface import IInit
from flaskavel.luminate.installer.output import Output
from flaskavel.luminate.installer.setup import Setup
from flaskavel.luminate.installer.upgrade import Upgrade

class Init(IInit):
    """
    Class responsible for handling initialization, upgrading, and creating new applications.

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

    def __init__(self, output=Output, upgrade=Upgrade):
        """
        Initializes the class with the necessary components.

        Parameters
        ----------
        output : Output, optional
            The object to handle output (defaults to the Output class).
        upgrade : Upgrade, optional
            The object to handle the upgrade process (defaults to the Upgrade class).
        """
        self.output = output
        self.upgrade = upgrade

    def displayVersion(self):
        """
        Displays the current version of the Framework using ASCII art.

        If an error occurs while trying to display the ASCII art, the exception is caught
        and an error message is shown.
        """
        try:
            self.output.asciiIco()
        except Exception as e:
            self.output.error(f"Fatal Error: {e}")

    def executeUpgrade(self):
        """
        Executes the upgrade process to the most recent version of the Framework.

        A message indicating the start of the process is printed, followed by the execution of the upgrade.
        If an error occurs during the upgrade process, the exception is caught
        and an error message is shown.
        """
        try:
            self.output.info("Starting the upgrade process...")
            self.upgrade.execute()
            self.output.asciiIco()
        except Exception as e:
            self.output.error(f"Fatal Error: {e}")

    def createNewApp(self, name_app: str = 'example-app'):
        """
        Creates a new application with the provided name.

        Parameters
        ----------
        name_app : str, optional
            The name of the new application (defaults to 'example-app').

        If an error occurs during the creation of the application, the exception is caught
        and an error message is shown.
        """
        try:
            self.output.startInstallation()
            Setup(output=self.output, name_app=name_app).handle()
            self.output.endInstallation()
        except Exception as e:
            self.output.error(f"Fatal Error: {e}")

    def displayInfo(self):
        """
        Displays additional information, including ASCII art.

        If an error occurs while trying to display the ASCII art, the exception is caught
        and an error message is shown.
        """
        try:
            self.output.asciiInfo()
        except Exception as e:
            self.output.error(f"Fatal Error: {e}")
