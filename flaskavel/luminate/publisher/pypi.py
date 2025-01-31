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
    """

    def __init__(self, token: str = None):
        """
        Initializes the class with an authentication token.
        """
        self.token = token or os.getenv("PYPI_TOKEN").strip()
        self.python_path = sys.executable
        self.project_root = os.getcwd()
        self.clearRepository()

    def gitPush(self):
        """
        Commits and pushes changes to the Git repository if there are modifications.
        """
        # Aseguramos que los comandos de Git se ejecuten desde la raíz del proyecto
        git_status = subprocess.run(
            ["git", "status", "--short"], capture_output=True, text=True, cwd=self.project_root
        )
        modified_files = git_status.stdout.strip()

        if modified_files:
            Console.info("📌 Staging files for commit...")
            subprocess.run(
                ["git", "add", "."], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.project_root
            )

            Console.info(f"✅ Committing changes: '📦 Release version {VERSION}'")
            subprocess.run(
                ["git", "commit", "-m", f"📦 Release version {VERSION}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.project_root
            )

            Console.info("🚀 Pushing changes to the remote repository...")
            subprocess.run(
                ["git", "push", "-f"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.project_root
            )
        else:
            Console.info("✅ No changes to commit.")

    def build(self):
        """
        Compiles the package using `setup.py` to generate distribution files.
        """
        try:
            Console.info("🛠️ Building the package...")

            # Ensure setup.py exists in the current working directory
            setup_path = os.path.join(self.project_root, "setup.py")
            if not os.path.exists(setup_path):
                Console.error("❌ Error: setup.py not found in the current execution directory.")
                return

            # Run the build command
            subprocess.run(
                [self.python_path, "setup.py", "sdist", "bdist_wheel"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.project_root
            )

            Console.success("✅ Build process completed successfully!")
        except subprocess.CalledProcessError as e:
            Console.error(f"❌ Build failed: {e}")

    def publish(self):
        """
        Uploads the package to PyPI using Twine.
        """
        token = self.token
        if not token:
            Console.error("❌ Error: PyPI token not found in environment variables.")
            return

        # Find Twine in the virtual environment path
        twine_path = os.path.join(self.project_root, 'venv', 'Scripts', 'twine')
        twine_path = os.path.abspath(twine_path)

        Console.info("📤 Uploading package to PyPI...")
        subprocess.run(
            [twine_path, "upload", "dist/*", "-u", "__token__", "-p", token],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.project_root
        )

        Console.info("🧹 Cleaning up temporary files...")
        subprocess.run(
            ["powershell", "-Command", "Get-ChildItem -Recurse -Filter *.pyc | Remove-Item; Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse"],
            check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.project_root
        )
        self.clearRepository()
        Console.success("✅ Publishing process completed successfully!")

    def clearRepository(self):
        """
        Deletes temporary directories created during the publishing process.
        """
        folders = ["build", "dist", "flaskavel.egg-info"]
        for folder in folders:
            folder_path = os.path.join(self.project_root, folder)
            if os.path.exists(folder_path):
                try:
                    shutil.rmtree(folder_path)
                except PermissionError:
                    Console.error(f"❌ Error: Could not remove {folder_path} due to insufficient permissions.")
                except Exception as e:
                    Console.error(f"❌ Error removing {folder_path}: {str(e)}")
