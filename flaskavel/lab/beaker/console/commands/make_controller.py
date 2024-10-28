import os
import re
from pathlib import Path
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.beaker.paths.helpers import app_path

@reactor.register
class MakeController(Command):
    """
    Command to create a new controller file within the Flaskavel application.
    """

    # Command signature for execution
    signature: str = 'make:controller'

    # Brief description of the command
    description: str = 'Create a controller'

    def arguments(self) -> list:
        """
        Defines the command-line arguments for the 'make:controller' command.

        Returns:
            list: Command argument specifications.
        """
        return [
            ('--name', {'type': str, 'required': True, 'help': 'Create a controller into "app/Http/Controllers/" folder.'})
        ]

    def handle(self) -> None:
        """
        Executes the 'make:controller' command, creating a new controller file based on a template.

        Raises:
            ValueError: If controller name is invalid or already exists.
        """
        try:
            # Retrieve the controller name argument
            name: str = self.argument('name')
            controllers_base_path = app_path('Http/Controllers')

            # Separate subfolders and file name if present in the provided path
            if '/' in name:
                # Separate into folders and file name
                *subfolders, controller_name = name.strip("/").split("/")
                sub_path = os.path.join(controllers_base_path, *subfolders)
            else:
                # If no subfolders, assign base path
                sub_path = controllers_base_path
                controller_name = name

            # Remove spaces in the controller name
            controller_name = controller_name.replace(" ", "")

            # Regex pattern to validate the controller name (alphabetic and underscores only)
            pattern = r'^[a-zA-Z_]+$'

            # Validate the controller name against the pattern
            if not re.match(pattern, controller_name):
                raise ValueError("Controller name must only contain alphabetic characters and underscores (_), no numbers or special characters are allowed.")

            # Create subdirectory if it does not exist
            os.makedirs(sub_path, exist_ok=True)

            # Check if the controller file already exists in the specified directory
            controller_filename = f"{controller_name}.py"
            existing_files = [f.lower() for f in os.listdir(sub_path) if os.path.isfile(os.path.join(sub_path, f))]

            if controller_filename.lower() in existing_files:
                raise ValueError(f"A controller with the name '{controller_name}' already exists in the directory: {sub_path}")

            # Load template and create new controller file with modified content
            template_path = os.path.join(f'{Path(__file__).resolve().parent.parent}/stub/Controller.stub')
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()

            # Replace placeholders in the template with the controller name
            controller_content = template_content.replace('{{name-controller}}', controller_name)

            # Write the final controller content to the new controller file
            new_controller_path = os.path.join(sub_path, controller_filename)
            with open(new_controller_path, 'w') as new_file:
                new_file.write(controller_content)

            # Display success message with path
            self.info(f"Controller '{controller_name}' created successfully in {sub_path}")

        except ValueError as e:
            # Display error message for invalid input
            self.error(f"Error: {e}")

        except Exception as e:
            # Display general error message for any unexpected issue
            self.error(f"An unexpected error occurred: {e}")
