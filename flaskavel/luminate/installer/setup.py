import re
import os
import sys
import shutil
import tempfile
import subprocess
from unicodedata import normalize
from flaskavel.framework import SKELETON, DOCS
from flaskavel.luminate.installer.output import Output
from flaskavel.luminate.contracts.installer.setup_interface import ISetup

class Setup(ISetup):
    """
    A class to initialize a Flaskavel project by performing the following setup actions:
    1. Sanitize the folder name.
    2. Clone the repository.
    3. Create a virtual environment.
    4. Install dependencies from requirements.txt.
    5. Set up .env configuration.
    6. Generate an API key.
    7. Clean up temporary files and .git origin.

    Parameters
    ----------
    output : Output
        An instance of Output, used to display messages to the console.
    name_app : str, optional
        The name of the app to create. If not provided, defaults to "{NAME}_app".

    Attributes
    ----------
    output : Output
        An instance of Output used for logging information.
    name_app_folder : str
        The sanitized folder name for the application.
    """

    def __init__(self, name: str = 'example-app', output = Output):
        """
        Initialize FlaskavelInit class.

        Parameters
        ----------
        output : Output
            An instance of Output to handle logging.
        name_app : str, optional
            Name of the application. If not provided, defaults to "example-app".
        """
        self.output = output
        self.output.startInstallation()
        self.name_app_folder = self._sanitize_folder_name(name)

    def _sanitize_folder_name(self, name: str) -> str:
        """
        Sanitize the provided folder name to ensure it is valid across different operating systems.

        Steps:
        1. Normalize text to remove accents and special characters.
        2. Convert to lowercase.
        3. Replace spaces with underscores.
        4. Remove invalid characters.
        5. Strip leading and trailing whitespace.
        6. Enforce length limit (255 characters).
        7. Ensure the result contains only valid characters.

        Parameters
        ----------
        name : str
            The original folder name to sanitize.

        Returns
        -------
        str
            The sanitized folder name.

        Raises
        ------
        ValueError
            If the sanitized folder name is empty or contains invalid characters.
        """
        if not name:
            self.output.error("Folder name cannot be empty.")

        # Strip leading and trailing whitespace
        name = name.strip()

        # Normalize to remove accents and special characters
        name = normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")

        # Convert to lowercase
        name = name.lower()

        # Replace spaces with underscores
        name = name.replace(" ", "_")

        # Remove invalid characters for folder names
        name = re.sub(r'[\\/:*?"<>|]', '', name)

        # Limit the length to 255 characters
        name = name[:255]

        # Validate against allowed characters
        if not re.match(r'^[a-z0-9_-]+$', name):
            self.output.error("The folder name can only contain letters, numbers, underscores, and hyphens.")

        if not name:
            self.output.error("The sanitized folder name is empty after processing.")

        return name

    def handle(self):
        """
        Executes the setup process for initializing the Flaskavel project.

        This process includes:
        1. Cloning the repository.
        2. Creating a virtual environment.
        3. Installing dependencies from requirements.txt.
        4. Setting up the .env file.
        5. Generating an API key.
        6. Cleaning up temporary files and .git remote origin.

        Raises
        ------
        ValueError
            If there is an error during any subprocess execution.
        Exception
            If any unexpected error occurs.
        """
        try:
            # Validate Folder
            if os.path.exists(self.name_app_folder) and os.path.isdir(self.name_app_folder):
                self.output.error(f"The folder '{self.name_app_folder}' already exists.")

            # Clone the repository
            self.output.info(f"Cloning the repository into '{self.name_app_folder}'... (Getting Latest Version)")
            subprocess.run(["git", "clone", SKELETON, self.name_app_folder], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.output.info(f"Repository successfully cloned into '{self.name_app_folder}'.")

            # Change to the project directory
            project_path = os.path.join(os.getcwd(), self.name_app_folder)
            os.chdir(project_path)
            self.output.info(f"Entering directory '{self.name_app_folder}'.")

            # Create a virtual environment
            self.output.info("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.output.info("Virtual environment successfully created.")

            # Virtual environment path
            venv_path = os.path.join(project_path, "venv", "Scripts" if os.name == "nt" else "bin")

            # Check if requirements.txt exists
            if not os.path.exists("requirements.txt"):
                self.output.error(f"'requirements.txt' not found. Please visit the Flaskavel Docs for more details: {DOCS}")

            # Install dependencies from requirements.txt
            self.output.info("Installing dependencies from 'requirements.txt'...")
            subprocess.run([os.path.join(venv_path, "pip"), "install", "-r", "requirements.txt"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.output.info("Dependencies successfully installed.")

            # Create .env
            example_env_path = os.path.join(project_path, '.env.example')
            env_path = os.path.join(project_path, '.env')
            shutil.copy(example_env_path, env_path)

            # Create ApiKey
            os.chdir(project_path)
            subprocess.run([sys.executable, '-B', 'reactor', 'key:generate'], capture_output=True, text=True)

            # Remove .git origin
            subprocess.run(["git", "remote", "remove", "origin"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Invalidate Cache File
            try:
                temp_dir = tempfile.gettempdir()
                for filename in os.listdir(temp_dir):
                    if filename.endswith('started.lab'):
                        file_path = os.path.join(temp_dir, filename)
                        os.remove(file_path)
            except Exception as e:
                self.output.fail("Unable to delete temporary files created by the framework on the device.")

            # Finish Process Message
            self.output.info(f"Project '{self.name_app_folder}' successfully created at '{os.path.abspath(project_path)}'.")
            self.output.endInstallation()

        except subprocess.CalledProcessError as e:
            self.output.error(f"Error while executing command: {e}")
        except Exception as e:
            self.output.error(f"An unexpected error occurred: {e}")
