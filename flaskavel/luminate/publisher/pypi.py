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
        self.working_dir = os.getcwd()
        self.python_path = sys.executable 

    def gitPush(self):
        """
        Commits and pushes changes to the Git repository if there are modifications.
        """
        git_status = subprocess.run(
            ["git", "status", "--short"], capture_output=True, text=True, cwd=self.working_dir
        )
        modified_files = git_status.stdout.strip()

        if modified_files:
            Console.info("📌 Staging files for commit...")
            subprocess.run(["git", "add", "."], check=True, cwd=self.working_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            Console.info(f"✅ Committing changes: '📦 Release version {VERSION}'")
            subprocess.run(["git", "commit", "-m", f"📦 Release version {VERSION}"], check=True, cwd=self.working_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            Console.info("🚀 Pushing changes to the remote repository...")
            subprocess.run(["git", "push", "-f"], check=True, cwd=self.working_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            Console.info("✅ No changes to commit.")

    def build(self):
        """
        Compiles the package using `setup.py` to generate distribution files.

        This process creates both source (`sdist`) and wheel (`bdist_wheel`) distributions.
        """
        try:
            Console.info("🛠️ Building the package...")

            # Ensure setup.py exists in the working directory
            setup_path = os.path.join(self.working_dir, "setup.py")
            if not os.path.exists(setup_path):
                Console.error("❌ Error: setup.py not found in the current execution directory.")
                return

            # Run the build command
            subprocess.run([self.python_path, "setup.py", "sdist", "bdist_wheel"], check=True, cwd=self.working_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

        # 🔍 Encuentra Twine automáticamente dentro del entorno virtual
        twine_path = os.path.join(os.path.dirname(self.python_path), "twine")
        print(twine_path)
        exit(1)

        # ⚠️ Verificar si Twine existe en la ubicación esperada
        if not os.path.exists(twine_path):
            Console.warning(f"⚠️ Twine not found at {twine_path}. Trying global Twine...")
            twine_path = shutil.which("twine")

        if not twine_path:
            Console.error("❌ Error: Twine not found. Install it with `pip install twine`.")
            return

        Console.info("📤 Uploading package to PyPI...")
        subprocess.run(
            [twine_path, "upload", "dist/*", "-u", "__token__", "-p", token],
            check=True, cwd=self.working_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        Console.info("🧹 Cleaning up temporary files...")
        subprocess.run(
            ["powershell", "-Command", "Get-ChildItem -Recurse -Filter *.pyc | Remove-Item; Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse"],
            check=True, cwd=self.working_dir, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
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
            folder_path = os.path.join(self.working_dir, folder)
            if os.path.exists(folder_path):
                Console.info(f"🗑️ Removing {folder_path}...")
                try:
                    shutil.rmtree(folder_path)
                except PermissionError:
                    Console.error(f"❌ Error: Could not remove {folder_path} due to insufficient permissions.")
                except Exception as e:
                    Console.error(f"❌ Error removing {folder_path}: {str(e)}")
        Console.success("✅ Cleanup completed.")
