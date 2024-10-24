from flaskavel.lab.catalyst.config import Config

class FlaskavelRunner:
    """Main runner for the Flaskavel application."""

    def __init__(self, basePath):
        """Initialize FlaskavelRunner with the base path.

        Args:
            basePath: The base path for the application.
        """
        self._basePath =basePath

    def handleRequest(self, debug:bool=None, port:int=5000, use_reloader:bool=False):
        """Handle an incoming request.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: Returns True indicating the request has been handled.
        """
        from flaskavel.lab.nucleus.http.kernel import Kernel
        return Kernel().handle(
            debug = debug or Config.app('debug'),
            port = port,
            use_reloader = use_reloader,
            load_dotenv = False
        )

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