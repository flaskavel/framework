import os
import re
from pathlib import Path
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.beaker.paths.helpers import app_path

@reactor.register
class MakeController(Command):
    """
    Command to create a new controller.
    """

    signature: str = 'make:controller'
    description: str = 'Create a controller'

    def arguments(self) -> list:
        """
        Defines the command-line arguments for the 'make:controller' command.
        """
        return [
            ('--name', {'type': str, 'required': True, 'default': True, 'help': 'Create a controller into "app/Http/Controllers/" folder.'})
        ]

    def handle(self) -> None:

        """
        Handles the execution of the 'make:controller' command to create a controller.
        """

        try:

            # Retrieve the argument
            name: str = self.argument('name')
            controllers_base_path = app_path('Http/Controllers')

            # Separate route and filename
            if '/' in name:
                # Separate into folders and file name
                *subfolders, controller_name = name.strip("/").split("/")
                sub_path = os.path.join(controllers_base_path, *subfolders)
            else:
                # If no subfolders, assign base path
                sub_path = controllers_base_path
                controller_name = name

            # Clean spaces only in the controller file name
            controller_name = controller_name.replace(" ", "")

            # Regex pattern that allows only alphabetic characters and underscores
            pattern = r'^[a-zA-Z_]+$'

            # Validate controller name against the pattern
            if not re.match(pattern, controller_name):
                raise ValueError("Controller name must only contain alphabetic characters and underscores (_), no numbers or special characters are allowed.")

            # Create the subdirectory if it doesn't exist
            os.makedirs(sub_path, exist_ok=True)

            # Verify if the name file already exists
            controller_filename = f"{controller_name}.py"
            existing_files = [f.lower() for f in os.listdir(sub_path) if os.path.isfile(os.path.join(sub_path, f))]

            if controller_filename.lower() in existing_files:
                raise ValueError(f"A controller with the name '{controller_name}' already exists in the directory: {sub_path}")

            # Read the stub, replace {{name-Controller}}, and create a new controller file
            template_path = os.path.join(f'{Path(__file__).resolve().parent.parent}/stub/Controller.stub')
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()

            # Replace {{name-Controller}} with the controller name
            controller_content = template_content.replace('{{name-Controller}}', controller_name)

            # Create and save the new controller file
            new_controller_path = os.path.join(sub_path, controller_filename)
            with open(new_controller_path, 'w') as new_file:
                new_file.write(controller_content)

            self.info(f"Controller '{controller_name}' created successfully in {sub_path}")

        except ValueError as e:
            raise ValueError(f"Error: {e}")

        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")
