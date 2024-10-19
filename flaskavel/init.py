import os
import re
import sys
import argparse
import subprocess
from flaskavel.lab.beaker.console.output import Console
from flaskavel.metadata import SKELETON, VERSION

class CreateApp:

    def __init__(self, name_app: str):
        # Convert the name to lowercase, replace spaces with underscores, and strip surrounding whitespace
        self.name_app = str(name_app).strip().replace(' ', '-').lower()

        # Git Repo Skeleton
        self.skeleton_repo = SKELETON

    def create(self):
        try:
            # Validate the application name with regex
            if not re.match(r'^[a-zA-Z0-9_]+(-[a-zA-Z0-9_]+)*$', self.name_app):
                raise ValueError("The application name can only contain letters, numbers, and underscores. Special characters and accents are not allowed.")

            # Clone the repository
            Console.info(
                message=f"Initiating cloning of the repository into '{self.name_app}'... ",
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
                message=f"Navigating to directory '{self.name_app}'.",
                timestamp=True
            )

            # Create a virtual environment
            Console.info(
                message="Creating a virtual environment... ",
                timestamp=True
            )
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            Console.info(
                message="Virtual environment successfully established.",
                timestamp=True
            )

            # Virtual environment path
            venv_path = os.path.join(project_path, "venv", "Scripts" if os.name == "nt" else "bin")

            # Install dependencies from requirements.txt
            Console.info(
                message="Commencing installation of dependencies from 'requirements.txt'... ",
                timestamp=True
            )
            subprocess.run([os.path.join(venv_path, "pip"), "install", "-r", "requirements.txt"], check=True)
            Console.info(
                message="Dependencies successfully installed.",
                timestamp=True
            )

            # Create .env
            env_path = os.path.join(project_path, '.env')
            env_path_example = os.path.join(project_path, '.env.example')

            # Read .env.example
            with open(env_path_example, 'r') as env_example_file:
                content_env = env_example_file.read()

            # Write .env
            with open(env_path, 'w') as env_file:
                env_file.write(content_env)

            Console.info(
                message="The .env file has been successfully created.",
                timestamp=True
            )

            # remove .git origin
            subprocess.run(["git", "remote", "remove", "origin"], check=True)

            Console.info(
                message=f"Project '{self.name_app}' has been successfully established at '{os.path.abspath(project_path)}'.",
                timestamp=True
            )

        except subprocess.CalledProcessError as e:
            Console.error(
                message=f"An error occurred while executing a command: {e}",
                timestamp=True
            )
            Console.newLine()
            sys.exit(1)

        except Exception as e:
            Console.error(
                message=f"An unexpected error has occurred: {e}",
                timestamp=True
            )
            Console.newLine()
            sys.exit(1)

def main():
    # Startup message
    Console.newLine()
    Console.info(
        message=f"Thank you for choosing Flaskavel v{VERSION}. Welcome aboard.",
        timestamp=True
    )

    # Create the argument parser
    parser = argparse.ArgumentParser(description="Flaskavel Application Creation Tool")

    # Required 'new' command and app name
    parser.add_argument('command', choices=['new'], help="The command must be 'new'.")
    parser.add_argument('name_app', help="The name of the Flaskavel application to be created.")

    # Parse the arguments
    try:
        # Parse the arguments
        args = parser.parse_args()

    except SystemExit as e:
        # This block captures the default behavior of argparse when invalid or missing arguments occur.
        # Customize the error message here
        Console.error(
            message="Invalid arguments detected. Example usage: 'flaskavel new example_app'",
            timestamp=True
        )
        Console.newLine()
        sys.exit(1)

    # Validate command (this is already done by 'choices')
    if args.command != 'new':
        Console.error(
            message="Unrecognized command. Did you mean 'flaskavel new example.app'?",
            timestamp=True
        )
        Console.newLine()
        sys.exit(1)

    # Validate app name (empty check is not needed because argparse handles that)
    if not args.name_app:
        Console.error(
            message="You must specify an application name. Did you mean 'flaskavel new example.app'?",
            timestamp=True
        )
        Console.newLine()
        sys.exit(1)

    # Create and run the app
    app = CreateApp(name_app=args.name_app)
    app.create()

if __name__ == "__main__":
    main()
