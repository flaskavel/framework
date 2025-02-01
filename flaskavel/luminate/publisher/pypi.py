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

    This class automates the process of committing changes to a Git repository, building a Python package,
    uploading it to PyPI, and cleaning up temporary files. It requires a PyPI authentication token.

    Methods
    -------
    __init__(token: str = None)
        Initializes the class with an optional PyPI authentication token.

    gitPush()
        Commits and pushes changes to the Git repository if modifications are detected.

    build()
        Compiles the package using `setup.py` to generate distribution files.

    publish()
        Uploads the package to PyPI using Twine.

    clearRepository()
        Deletes temporary directories created during the publishing process.
    """

    def __init__(self, token: str = None):
        """
        Initializes the class with an authentication token.

        Parameters
        ----------
        token : str, optional
            Authentication token for PyPI. If not provided, it is retrieved from environment variables.

        Attributes
        ----------
        token : str
            The PyPI authentication token.
        python_path : str
            The path to the Python interpreter used in the environment.
        project_root : str
            The root directory of the project where the process is executed.
        """
        self.token = token or os.getenv("PYPI_TOKEN").strip()
        self.python_path = sys.executable
        self.project_root = os.getcwd()
        self.clearRepository()

    def gitPush(self):
        """
        Commits and pushes changes to the Git repository if there are modifications.

        This method checks for uncommitted changes and stages, commits, and pushes them
        to the remote Git repository.

        If there are no changes, it logs a message indicating no commits are necessary.

        Raises
        ------
        subprocess.CalledProcessError
            If any of the subprocess calls to Git fail.
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

        This method runs the `setup.py` script to generate both source (`sdist`)
        and wheel (`bdist_wheel`) distribution formats for the package.

        Raises
        ------
        subprocess.CalledProcessError
            If the `setup.py` command fails.
        """
        try:
            Console.info("🛠️  Building the package...")

            # Ensure setup.py exists in the current working directory
            setup_path = os.path.join(self.project_root, "setup.py")
            if not os.path.exists(setup_path):
                Console.error("❌ Error: setup.py not found in the current execution directory.")
                return

            # Run the build command
            subprocess.run(
                [self.python_path, "setup.py", "sdist", "bdist_wheel"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.project_root
            )

            Console.info("✅ Build process completed successfully!")
        except subprocess.CalledProcessError as e:
            Console.error(f"❌ Build failed: {e}")

    def publish(self):
        """
        Uploads the package to PyPI using Twine.

        This method uses the `twine` command to upload the built distribution files
        from the `dist/` folder to the PyPI repository.

        Parameters
        ----------
        token : str
            The PyPI authentication token, which is passed during the initialization.

        Raises
        ------
        subprocess.CalledProcessError
            If the Twine command fails during the upload process.
        ValueError
            If no token is provided for authentication.
        """
        token = self.token
        if not token:
            Console.error("❌ Error: PyPI token not found in environment variables.")
            return

        # Find Twine in the virtual environment path
        twine_path = os.path.join(self.project_root, 'venv', 'Scripts', 'twine')
        twine_path = os.path.abspath(twine_path)

        Console.info("📤 Uploading package to PyPI...")
        try:
            subprocess.run(
                [twine_path, "upload", "dist/*", "-u", "__token__", "-p", token],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.project_root
            )
        except Exception as e:
            Console.fail("🔴 Error loading the package. Try changing the version and retry.")
            Console.warning("⛔ If the issue persists, review the script in detail.")
            exit()

        Console.info("🧹 Cleaning up temporary files...")
        subprocess.run(
            ["powershell", "-Command", "Get-ChildItem -Recurse -Filter *.pyc | Remove-Item; Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse"],
            check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.project_root
        )
        self.clearRepository()
        Console.success(f"✅ [v{VERSION}] - Publishing process completed successfully!")

    def clearRepository(self):
        """
        Deletes temporary directories created during the publishing process.

        This method removes the following directories from the project root:
        - `build/`
        - `dist/`
        - `flaskavel.egg-info/`

        Raises
        ------
        PermissionError
            If the method fails to delete any of the directories due to insufficient permissions.
        Exception
            If any other error occurs during the deletion process.
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
