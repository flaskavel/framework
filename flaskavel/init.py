import os
import re
import sys
import shutil
import tempfile
import argparse
import subprocess
from flaskavel.lab.beaker.console.output import Console

class FlaskavelInit:

    def __init__(self, name_app: str):

        # Convert the name to lowercase, replace spaces with underscores, and strip surrounding whitespace
        self.name_app = str(name_app).lower().replace(" ", "_").strip()

        # Git Repo Skeleton.
        self.skeleton_repo = "https://github.com/flaskavel/skeleton"

    def create(self):

        try:

            # Validate the application name with regex
            if not re.match(r'^[a-zA-Z0-9_-]+$', self.name_app):
                raise ValueError("The application name can only contain letters, numbers, underscores, and hyphens. Special characters and accents are not allowed.")


            # Clone the repository
            Console.info(
                message=f"Cloning the repository into '{self.name_app}'... (Getting Latest Version)",
                timestamp=True
            )

            subprocess.run(["git", "clone", self.skeleton_repo, self.name_app], check=True)

            Console.info(
                message=f"Repository successfully cloned into '{self.name_app}'.",
                timestamp=True
            )

            # Change to the project directory
            project_path = os.path.join(os.getcwd(), self.name_app)
            os.chdir(project_path)
            Console.info(
                message=f"Entering directory '{self.name_app}'.",
                timestamp=True
            )

            # Create a virtual environment
            Console.info(
                message="Creating virtual environment...",
                timestamp=True
            )

            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

            Console.info(
                message="Virtual environment successfully created.",
                timestamp=True
            )

            # Virtual environment path
            venv_path = os.path.join(project_path, "venv", "Scripts" if os.name == "nt" else "bin")

            # Check if requirements.txt exists
            if not os.path.exists("requirements.txt"):
                Console.error(
                    message=f"'requirements.txt' not found. Please visit the Flaskavel repository for more details: {self.skeleton_repo}",
                    timestamp=True
                )

            else:

                # Install dependencies from requirements.txt
                Console.info(
                    message="Installing dependencies from 'requirements.txt'...",
                    timestamp=True
                )

                subprocess.run([os.path.join(venv_path, "pip"), "install", "-r", "requirements.txt"], check=True)

                Console.info(
                    message="Dependencies successfully installed.",
                    timestamp=True
                )

                # Create .env
                example_env_path = os.path.join(project_path,'.env.example')
                env_path = os.path.join(project_path,'.env')
                shutil.copy(example_env_path, env_path)

                # Create ApiKey
                os.chdir(project_path)
                subprocess.run(['python', '-B', 'reactor', 'key:generate'], capture_output=True, text=True)

                # remove .git origin
                subprocess.run(["git", "remote", "remove", "origin"], check=True)

                # Invalidate Cache
                temp_dir = tempfile.gettempdir()
                for filename in os.listdir(temp_dir):
                    if filename.endswith('started.lab'):
                        file_path = os.path.join(temp_dir, filename)
                        os.remove(file_path)

            Console.info(
                message=f"Project '{self.name_app}' successfully created at '{os.path.abspath(project_path)}'.",
                timestamp=True
            )

        except subprocess.CalledProcessError as e:
            Console.error(
                message=f"Error while executing command: {e}",
                timestamp=True
                )
            Console.newLine()
            sys.exit(1)

        except Exception as e:
            Console.error(
                message=f"An unexpected error occurred: {e}",
                timestamp=True
            )
            Console.newLine()
            sys.exit(1)

def main():

    # Startup message
    Console.newLine()
    Console.info(
        message="Thank you for using Flaskavel, welcome.",
        timestamp=True
    )

    # Create the argument parser
    parser = argparse.ArgumentParser(description="Flaskavel App Creation Tool")

    # Required 'new' command and app name
    parser.add_argument('command', choices=['new'], help="Command must be 'new'.")
    parser.add_argument('name_app', help="The name of the Flaskavel application to create.")

    # Parse the arguments
    try:
        # Parse the arguments
        args = parser.parse_args()

    except SystemExit as e:
        # This block captures the default behavior of argparse when invalid or missing arguments occur.
        # Customize the error message here
        Console.error(
            message="Invalid arguments. Usage example: 'flaskavel new example_app'",
            timestamp=True
        )
        Console.newLine()
        sys.exit(1)

    # Validate command (this is already done by 'choices')
    if args.command != 'new':
        Console.error(
            message="Unrecognized command, did you mean 'flaskavel new example.app'?",
            timestamp=True
        )
        Console.newLine()
        sys.exit(1)

    # Validate app name (empty check is not needed because argparse handles that)
    if not args.name_app:
        Console.error(
            message="You must specify an application name, did you mean 'flaskavel new example.app'?",
            timestamp=True
        )
        Console.newLine()
        sys.exit(1)

    # Create and run the app
    app = FlaskavelInit(name_app=args.name_app)
    app.create()

if __name__ == "__main__":
    main()