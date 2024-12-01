from flaskavel.lab.nucleus.http.kernel import Kernel as KernerHttp
from app.Console.Kernel import Kernel as KernelCLI # type: ignore

class FlaskavelRunner:
    """Main runner for the Flaskavel application."""

    def __init__(self, basePath, start_time):
        """Initialize FlaskavelRunner with the base path.

        Args:
            basePath: The base path for the application.
        """
        self._basePath =basePath
        self.start_time = start_time

    def handleRequestWSGI(self, environ, start_response):
        """
        Handle WSGI requests for production environments.

        This method wraps the WSGI app of the Flaskavel instance and handles the requests.

        Args:
            environ (dict): The WSGI environment.
            start_response (callable): The WSGI start_response callable.

        Returns:
            The response from the WSGI app.
        """
        return KernerHttp().handleProductionWSGI(
            environ=environ,
            start_response=start_response
        )

    def handleDevelopment(self, debug=True, port=5000, use_reloader=True, load_dotenv=False):
        """
        Start the Flaskavel application in development mode.

        This method runs the Flaskavel application with specified parameters for development purposes.

        Args:
            debug (bool, optional): Enables or disables debug mode. Defaults to True.
            port (int, optional): The port to run the development server on. Defaults to 5000.
            use_reloader (bool, optional): Enables or disables the reloader. Defaults to True.
            load_dotenv (bool, optional): Determines if environment variables from .env should be loaded. Defaults to False.

        Returns:
            None
        """
        return KernerHttp().handleDevelopment(
            debug=debug,
            port=port,
            use_reloader=use_reloader,
            load_dotenv=load_dotenv
        )

    def handleCommand(self, *args, **kwargs):
        """Handle a command execution within the application.

        This method initializes the Kernel class, sets the start time,
        the base path, and invokes the handle method to process the command.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        KernelCLI().handle(*args, **kwargs)