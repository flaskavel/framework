import os
import shutil
import subprocess
from flaskavel.luminate.console.output.console import Console
from flaskavel.luminate.contracts.publisher.pypi_publisher_repository import IPypiPublisher
from flaskavel.metadata import VERSION

class PypiPublisher(IPypiPublisher):
    """
    Handles the publishing process of a package to PyPI and repository management.

    Methods
    -------
    git_push():
        Adds, commits, and pushes changes to the Git repository if modifications are detected.

    publish():
        Uploads the package to PyPI using Twine.

    clear_repository():
        Deletes temporary directories created during the publishing process.
    """

    def __init__(self, token: str = None):
        """
        Initializes the class with an authentication token.

        Parameters
        ----------
        token : str
            Authentication token for PyPI.
        """
        self.token = token or os.getenv("PYPI_TOKEN")

    def gitPush(self):
        """
        Commits and pushes changes to the Git repository if there are modifications.
        """
        # Check repository status
        git_status = subprocess.run(
            ["git", "status", "--short"], capture_output=True, text=True
        )
        modified_files = git_status.stdout.strip()

        if modified_files:
            Console.info("📌 Staging files for commit...")
            subprocess.run(["git", "add", "."], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            Console.info(f"✅ Committing changes: '📦 Release version {VERSION}'")
            subprocess.run(["git", "commit", "-m", f"📦 Release version {VERSION}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            Console.info("🚀 Pushing changes to the remote repository...")
            subprocess.run(["git", "push", "-f"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            Console.info("✅ No changes to commit.")

    def publish(self):
        """
        Uploads the package to PyPI using Twine.

        The PyPI token is retrieved from the 'PYPI' environment variable.
        """
        token = os.getenv("PYPI")

        if not self.token:
            Console.error("❌ Error: PyPI token not found in environment variables.")
            return

        # Get Twine path within the virtual environment
        current_path = os.getcwd()
        twine_path = os.path.abspath(os.path.join(current_path, "venv", "Scripts", "twine"))

        if not os.path.exists(twine_path):
            Console.error(f"❌ Error: Twine not found at the expected path: {twine_path}")
            return

        Console.info("📤 Uploading package to PyPI...")
        subprocess.run(
            [twine_path, "upload", "dist/*", "-u", "__token__", "-p", token],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Clean temporary Python files (__pycache__, .pyc)
        Console.info("🧹 Cleaning up temporary files...")
        subprocess.run(
            ["powershell", "-Command", "Get-ChildItem -Recurse -Filter *.pyc | Remove-Item; Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse"],
            check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        Console.success("✅ Publishing process completed successfully!")

    def clearRepository(self):
        """
        Deletes temporary directories created during the publishing process.

        The following directories are removed:
        - build
        - dist
        - flaskavel.egg-info
        """
        folders = ["build", "dist", "flaskavel.egg-info"]
        for folder in folders:
            if os.path.exists(folder):
                Console.info(f"🗑️ Removing {folder}...")
                try:
                    shutil.rmtree(folder)
                except PermissionError:
                    Console.error(f"❌ Error: Could not remove {folder} due to insufficient permissions.")
                except Exception as e:
                    Console.error(f"❌ Error removing {folder}: {str(e)}")
        Console.success("✅ Cleanup completed.")
