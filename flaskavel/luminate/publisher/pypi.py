import os
import shutil
import subprocess
import sys
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

    build():
        Compiles the package using `setup.py` to generate distribution files.

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
        token : str, optional
            Authentication token for PyPI. If not provided, it is retrieved from environment variables.
        """
        self.token = token or os.getenv("PYPI_TOKEN")

    def gitPush(self):
        """
        Commits and pushes changes to the Git repository if there are modifications.
        """
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

    def build(self):
        """
        Compiles the package using `setup.py` to generate distribution files.

        This process creates both source (`sdist`) and wheel (`bdist_wheel`) distributions.
        """
        try:
            Console.info("🛠️ Building the package...")

            # Get the current Python interpreter path
            python_path = sys.executable

            # Ensure setup.py exists in the current directory
            setup_path = os.path.join(os.getcwd(), "setup.py")
            if not os.path.exists(setup_path):
                Console.error("❌ Error: setup.py not found in the current directory.")
                return

            # Run the build command
            subprocess.run([python_path, "setup.py", "sdist", "bdist_wheel"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            Console.success("✅ Build process completed successfully!")
        except subprocess.CalledProcessError as e:
            Console.error(f"❌ Build failed: {e}")

    def publish(self):
        """
        Uploads the package to PyPI using Twine.

        The PyPI token is retrieved from the 'PYPI' environment variable.
        """
        token = self.token

        if not token:
            Console.error("❌ Error: PyPI token not found in environment variables.")
            return

        # Get Twine path
        twine_path = os.path.join(os.path.abspath(os.getcwd()), "venv", "Scripts", "twine.*")

        if not os.path.exists(twine_path):
            Console.error(f"❌ Error: Twine not found at the expected path: {twine_path}")
            return

        Console.info("📤 Uploading package to PyPI...")
        subprocess.run(
            [twine_path, "upload", "dist/*", "-u", "__token__", "-p", token],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # Clean up temporary Python files (__pycache__, .pyc)
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
