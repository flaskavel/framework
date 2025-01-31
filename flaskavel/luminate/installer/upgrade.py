from flaskavel.luminate.contracts.installer.upgrade_interface import IUpgrade
import subprocess
import sys

class Upgrade(IUpgrade):
    """
    A class responsible for handling the upgrade process of Flaskavel.

    Methods
    -------
    execute() : None
        Executes the upgrade process to install the latest version of Flaskavel.
    """

    @staticmethod
    def execute():
        """
        Handle the --upgrade command to update Flaskavel to the latest version.

        This method attempts to upgrade Flaskavel using the pip package manager.
        It executes a command that installs the latest version of Flaskavel, ensuring
        the application is up-to-date.

        Raises
        ------
        ValueError
            If the upgrade process fails or encounters any error during execution.

        Notes
        -----
        The upgrade process uses `pip` via the command:
        `python -m pip install --upgrade flaskavel`.
        """
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "flaskavel"])
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Upgrade failed: {e}")
        except Exception as e:
            raise ValueError(e)
