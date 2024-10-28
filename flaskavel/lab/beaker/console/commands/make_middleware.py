import os
import re
from pathlib import Path
from flaskavel.lab.beaker.paths.helpers import app_path
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command

@reactor.register
class MakeMiddleware(Command):
    """
    Command to create a new middleware file within the Flaskavel application.
    """

    # Command signature for execution
    signature: str = 'make:middleware'

    # Brief description of the command
    description: str = 'Create a middleware'

    def arguments(self) -> list:
        """
        Defines the command-line arguments for the 'make:middleware' command.

        Returns:
            list: Command argument specifications.
        """
        return [
            ('--name', {'type': str, 'required': True, 'help': 'Create a middleware into "app/Http/Middlewares/" folder.'})
        ]

    def handle(self) -> None:
        """
        Executes the 'make:middleware' command, creating a new middleware file based on a template.

        Raises:
            ValueError: If middleware name is invalid or already exists.
        """
        try:
            # Retrieve the middleware name argument
            name: str = self.argument('name')
            middlewares_base_path = app_path('Http/Middlewares')

            # Separate subfolders and file name if present in the provided path
            if '/' in name:
                # Separate into folders and file name
                *subfolders, middleware_name = name.strip("/").split("/")
                sub_path = os.path.join(middlewares_base_path, *subfolders)
            else:
                # If no subfolders, assign base path
                sub_path = middlewares_base_path
                middleware_name = name

            # Remove spaces in the middleware name
            middleware_name = middleware_name.replace(" ", "")

            # Regex pattern to validate the middleware name (alphabetic and underscores only)
            pattern = r'^[a-zA-Z_]+$'

            # Validate the middleware name against the pattern
            if not re.match(pattern, middleware_name):
                raise ValueError("Middleware name must only contain alphabetic characters and underscores (_), no numbers or special characters are allowed.")

            # Create subdirectory if it does not exist
            os.makedirs(sub_path, exist_ok=True)

            # Check if the middleware file already exists in the specified directory
            middleware_filename = f"{middleware_name}.py"
            existing_files = [f.lower() for f in os.listdir(sub_path) if os.path.isfile(os.path.join(sub_path, f))]

            if middleware_filename.lower() in existing_files:
                raise ValueError(f"A middleware with the name '{middleware_name}' already exists in the directory: {sub_path}")

            # Load template and create new middleware file with modified content
            template_path = os.path.join(f'{Path(__file__).resolve().parent.parent}/stub/Middleware.stub')
            with open(template_path, 'r') as template_file:
                template_content = template_file.read()

            # Replace placeholders in the template with the middleware name
            middleware_content = template_content.replace('{{name-middleware}}', middleware_name)

            # Write the final middleware content to the new middleware file
            new_middleware_path = os.path.join(sub_path, middleware_filename)
            with open(new_middleware_path, 'w') as new_file:
                new_file.write(middleware_content)

            # Display success message with path
            self.info(f"Middleware '{middleware_name}' created successfully in {sub_path}")

        except ValueError as e:
            # Display error message for invalid input
            self.error(f"Error: {e}")

        except Exception as e:
            # Display general error message for any unexpected issue
            self.error(f"An unexpected error occurred: {e}")
