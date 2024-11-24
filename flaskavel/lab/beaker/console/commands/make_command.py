import os
import re
from pathlib import Path
from flaskavel.lab.beaker.paths.helpers import app_path
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command

@reactor.register
class MakeCommand(Command):
    """
    Command to create a new Command file within the Flaskavel application.
    """

    # Command signature for execution
    signature: str = 'make:command'

    # Brief description of the command
    description: str = 'Create a new command within the application'

    def arguments(self) -> list:
        """
        Defines the command-line arguments for the 'make:command' command.

        Returns:
            list: Command argument specifications.
        """
        return [
            ('--name', {'type': str, 'required': True, 'help': 'Create a command into "app/Console/Commands/" folder.'})
        ]

    def handle(self) -> None:
        """
        Executes the 'make:command' command, creating a new command file based on a template.

        Raises:
            ValueError: If command name is invalid or already exists.
        """
        try:
            # Retrieve the command name argument
            name: str = self.argument('name')
            controllers_base_path = app_path('Console/Commands')

            # Separate subfolders and file name if present in the provided path
            if '/' in name:
                # Separate into folders and file name
                *subfolders, command_name = name.strip("/").split("/")
                sub_path = os.path.join(controllers_base_path, *subfolders)
            else:
                # If no subfolders, assign base path
                sub_path = controllers_base_path
                command_name = name

            # Remove spaces in the command name
            command_name = command_name.replace(" ", "")

            # Regex pattern to validate the command name (alphabetic and underscores only)
            pattern = r'^[a-zA-Z_]+$'

            # Validate the command name against the pattern
            if not re.match(pattern, command_name):
                raise ValueError("Command name must only contain alphabetic characters and underscores (_), no numbers or special characters are allowed.")

            # Create subdirectory if it does not exist
            os.makedirs(sub_path, exist_ok=True)

            # Check if the command file already exists in the specified directory
            command_filename = f"{command_name}.py"
            existing_files = [f.lower() for f in os.listdir(sub_path) if os.path.isfile(os.path.join(sub_path, f))]

            if command_filename.lower() in existing_files:
                raise ValueError(f"A command with the name '{command_name}' already exists in the directory: {sub_path}")

            # Load template and create new command file with modified content
            template_path = os.path.join(f'{Path(__file__).resolve().parent.parent}/stub/Command.stub')
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()

            # Replace placeholders in template with command name details
            command_content = template_content.replace('{{name-command}}', command_name)\
                                              .replace('{{signature-name-command}}', command_name.lower()\
                                              .replace('command',''))

            # Write the final command content to the new command file
            new_command_path = os.path.join(sub_path, command_filename)
            with open(new_command_path, 'w') as new_file:
                new_file.write(command_content)

            # Display success message with path
            self.info(f"Command '{command_name}' created successfully in {sub_path}", timestamp=True)

        except ValueError as e:
            # Display error message for invalid input
            self.error(f"Error: {e}", timestamp=True)
            exit(1)

        except Exception as e:
            # Display general error message for any unexpected issue
            self.error(f"An unexpected error occurred: {e}", timestamp=True)
            exit(1)
