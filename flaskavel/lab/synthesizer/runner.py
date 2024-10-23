import time

class FlaskavelRunner:
    """Main runner for the Flaskavel application."""

    def __init__(self, basePath):
        """Initialize FlaskavelRunner with the base path.

        Args:
            basePath: The base path for the application.
        """
        self._basePath =basePath

    def handleRequest(self, *args, **kwargs):
        """Handle an incoming request.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: Returns True indicating the request has been handled.
        """
        return True

    def handleCommand(self, *args, **kwargs):
        """Handle a command execution within the application.

        This method initializes the Kernel class, sets the start time,
        the base path, and invokes the handle method to process the command.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        from app.Console.Kernel import Kernel # type: ignore
        kernel = Kernel()
        kernel.set_start_time(time.time())
        kernel.set_base_path(str(self._basePath))
        kernel.handle(*args, **kwargs)