import os
import re
from pathlib import Path
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.beaker.paths.helpers import app_path

@reactor.register
class MakeCommand(Command):
    """
    Command to create a new Command.
    """

    signature: str = 'make:command'
    description: str = 'Create a command'

    def arguments(self) -> list:
        """
        Defines the command-line arguments for the 'make:controller' command.
        """
        return [
            ('--name', {'type': str, 'required': True, 'help': 'Create a command into "app/Console/Commands/" folder.'})
        ]

    def handle(self) -> None:

        """
        Handles the execution of the 'make:command' command to create a command.
        """

        try:

            # Retrieve the argument
            name: str = self.argument('name')
            controllers_base_path = app_path('Console/Commands')

            # Separate route and filename
            if '/' in name:
                # Separate into folders and file name
                *subfolders, command_name = name.strip("/").split("/")
                sub_path = os.path.join(controllers_base_path, *subfolders)
            else:
                # If no subfolders, assign base path
                sub_path = controllers_base_path
                command_name = name

            # Clean spaces only in the file name
            command_name = command_name.replace(" ", "")

            # Regex pattern that allows only alphabetic characters and underscores
            pattern = r'^[a-zA-Z_]+$'

            # Validate name against the pattern
            if not re.match(pattern, command_name):
                raise ValueError("Command name must only contain alphabetic characters and underscores (_), no numbers or special characters are allowed.")

            # Create the subdirectory if it doesn't exist
            os.makedirs(sub_path, exist_ok=True)

            # Verify if the name file already exists
            command_filename = f"{command_name}.py"
            existing_files = [f.lower() for f in os.listdir(sub_path) if os.path.isfile(os.path.join(sub_path, f))]

            if command_filename.lower() in existing_files:
                raise ValueError(f"A command with the name '{command_name}' already exists in the directory: {sub_path}")

            # Read the stub, replace var, and create a new file
            template_path = os.path.join(f'{Path(__file__).resolve().parent.parent}/stub/Command.stub')
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()

            # Replace var with the name
            command_content = template_content.replace('{{name-command}}', command_name).replace('{{signature-name-command}}', command_name.lower().replace('command',''))

            # Create and save the new file
            new_command_path = os.path.join(sub_path, command_filename)
            with open(new_command_path, 'w') as new_file:
                new_file.write(command_content)

            self.info(f"Command '{command_name}' created successfully in {sub_path}")

        except ValueError as e:
            self.error(f"Error: {e}")

        except Exception as e:
            self.error(f"An unexpected error occurred: {e}")
