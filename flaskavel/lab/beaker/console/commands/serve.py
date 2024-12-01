import sys
from bootstrap.app import app  # type: ignore
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command

@reactor.register
class Serve(Command):
    """
    Command to start the Flaskavel development server.
    """

    # Command signature used to execute this command.
    signature: str = 'serve'

    # A brief description of the command.
    description: str = 'Starts the Flaskavel development server'

    def arguments(self) -> list:
        """
        Defines the command-line arguments for the 'serve' command.

        Returns:
            list: A list of argument tuples for the command.
        """
        return [
            ('--debug', {'type': bool, 'required': False, 'default': True, 'help': 'Enable or disable debug mode'}),
            ('--port', {'type': int, 'required': False, 'default': 5000, 'help': 'Port number for the server'}),
            ('--reload', {'type': bool, 'required': False, 'default': True, 'help': 'Enable or disable auto-reload on changes'}),
        ]

    def _validate_bool_argument(self, arg_value: any) -> bool:
        """
        Ensures the argument is correctly interpreted as a boolean.

        Args:
            arg_value (any): The value to validate.

        Returns:
            bool: The corresponding boolean value.
        """
        if isinstance(arg_value, bool):
            return arg_value
        if isinstance(arg_value, str):
            return arg_value.lower() in ['true', '1', 'yes']
        return False

    def handle(self) -> None:
        """
        Handles the execution of the 'serve' command by starting the development server.

        Retrieves arguments and starts the server. Exits the program with the server's status.
        """
        try:
            # Retrieve and validate arguments
            port: int = self.argument('port')
            debug: bool = self._validate_bool_argument(self.argument('debug'))
            use_reloader: bool = self._validate_bool_argument(self.argument('reload'))

            # Validate port range
            if not (1024 <= port <= 65535):
                raise ValueError(f"Invalid port number: {port}. Port must be between 1024 and 65535.")

            # Start the Flaskavel development server with the provided arguments
            status = app().handleDevelopment(
                debug=debug,
                port=port,
                use_reloader=use_reloader
            )

            # Exit with the server status code
            sys.exit(status)

        except ValueError as e:
            # Display error message for invalid input
            self.error(f"Error: {e}", timestamp=True)
            exit(1)

        except Exception as e:
            # Display general error message for any unexpected issue
            self.error(f"An unexpected error occurred: {e}", timestamp=True)
            exit(1)
