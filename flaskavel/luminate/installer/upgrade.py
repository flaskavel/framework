from flaskavel.luminate.contracts.installer.upgrade_interface import IUpgrade
import subprocess
import sys

class Upgrade(IUpgrade):

    @staticmethod
    def execute():
        """
        Handle the --upgrade command to update Flaskavel to the latest version.
        """
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "flaskavel"])
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Upgrade failed: {e}")
        except Exception as e:
            raise ValueError(e)