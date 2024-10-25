import os
import re
from pathlib import Path
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.beaker.paths.helpers import app_path

@reactor.register
class MakeMiddleware(Command):
    """
    Command to create a new middleware.
    """

    signature: str = 'make:middleware'
    description: str = 'Create a middleware'

    def arguments(self) -> list:
        """
        Defines the command-line arguments for the 'make:middleware' command.
        """
        return [
            ('--name', {'type': str, 'required': True, 'help': 'Create a middleware into "app/Http/Middleware/" folder.'})
        ]

    def handle(self) -> None:

        """
        Handles the execution of the 'make:middleware' command to create a middleware.
        """

        try:

            # Retrieve the argument
            name: str = self.argument('name')
            middlewares_base_path = app_path('Http/Middleware')

            # Separate route and filename
            if '/' in name:
                # Separate into folders and file name
                *subfolders, middleware_name = name.strip("/").split("/")
                sub_path = os.path.join(middlewares_base_path, *subfolders)
            else:
                # If no subfolders, assign base path
                sub_path = middlewares_base_path
                middleware_name = name

            # Clean spaces only in the file name
            middleware_name = middleware_name.replace(" ", "")

            # Regex pattern that allows only alphabetic characters and underscores
            pattern = r'^[a-zA-Z_]+$'

            # Validate name against the pattern
            if not re.match(pattern, middleware_name):
                raise ValueError("Middleware name must only contain alphabetic characters and underscores (_), no numbers or special characters are allowed.")

            # Create the subdirectory if it doesn't exist
            os.makedirs(sub_path, exist_ok=True)

            # Verify if the name file already exists
            middleware_filename = f"{middleware_name}.py"
            existing_files = [f.lower() for f in os.listdir(sub_path) if os.path.isfile(os.path.join(sub_path, f))]

            if middleware_filename.lower() in existing_files:
                raise ValueError(f"A middleware with the name '{middleware_name}' already exists in the directory: {sub_path}")

            # Read the stub, replace var, and create a new file
            template_path = os.path.join(f'{Path(__file__).resolve().parent.parent}/stub/Middleware.stub')
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()

            # Replace var with the name
            middleware_content = template_content.replace('{{name-command}}', middleware_name)

            # Create and save the new file
            new_middleware_path = os.path.join(sub_path, middleware_filename)
            with open(new_middleware_path, 'w') as new_file:
                new_file.write(middleware_content)

            self.info(f"Middleware '{middleware_name}' created successfully in {sub_path}")

        except ValueError as e:
            self.error(f"Error: {e}")

        except Exception as e:
            self.error(f"An unexpected error occurred: {e}")
