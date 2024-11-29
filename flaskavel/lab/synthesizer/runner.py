from flaskavel.lab.catalyst.config import Config

class FlaskavelRunner:
    """Main runner for the Flaskavel application."""

    def __init__(self, basePath, start_time):
        """Initialize FlaskavelRunner with the base path.

        Args:
            basePath: The base path for the application.
        """
        self._basePath =basePath
        self.start_time = start_time

    def handleRequest(self):
        """Handle an incoming request.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: Returns True indicating the request has been handled.
        """
        from flaskavel.lab.nucleus.http.kernel import Kernel
        return Kernel().handle()

    def handleCommand(self, *args, **kwargs):
        """Handle a command execution within the application.

        This method initializes the Kernel class, sets the start time,
        the base path, and invokes the handle method to process the command.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        from app.Console.Kernel import Kernel # type: ignore
        Kernel().handle(*args, **kwargs)