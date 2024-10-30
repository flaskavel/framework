import re
import time
import traceback
import typing as t
from flask import Flask
from flaskavel.lab.reagents.response import Response
from flaskavel.lab.beaker.console.output import Console
from flaskavel.lab.catalyst.exceptions import *

class Flaskavel(Flask):
    """A Flaskavel class that extends the Flask application to add custom error handling and console output."""

    def __init__(self, *args, **kwargs):
        """Initializes the Flaskavel application and sets up error handlers for global errors and 404 not found errors."""
        super(Flaskavel, self).__init__(*args, **kwargs)
        self.register_error_handler(Exception, self.handle_global_error)
        self.register_error_handler(404, self.handle_not_found)
        self.start_time = time.time()

    def handle_global_error(self, e):
        """
        Global error handler that logs exceptions and formats error messages.

        Args:
            e (Exception): The exception raised during runtime.

        Returns:
            Response: Custom response object with error details.
        """
        if isinstance(e, DumpFlaskavelException):
            Console.textDanger(message=f"Flaskavel Dump And Die")
            return Response.dd(
                data=e.response
            )

        if isinstance(e, AuthorizeFlaskavelException):
            Console.textDanger(message=f"Flaskavel Unauthorized Request")
            return Response.unauthorized(
                message=e.response
            )

        if isinstance(e, ValidateFlaskavelException):
            Console.textDanger(message=f"Flaskavel Unprocessable Entity")
            return Response.unprocessableEntity(
                errors=e.response.get('errors'),
                message=e.response.get('message')
            )

        # Convert the exception to a string and capture the traceback.
        error = str(e)
        traceback_list = traceback.format_tb(e.__traceback__)

        # Filter and format the traceback details, excluding Flask and Werkzeug internals.
        traceback_list_errors = []
        for trace in traceback_list:
            if '\\flask\\' not in trace and '\\werkzeug\\' not in trace:
                traceback_list_errors.append(
                    (re.sub(r'\s+', ' ', trace.strip().replace('\n', ' - ').replace('^', ' '))).strip(' - ')
                )

        # Log the error details in the console with timestamped output.
        Console.textDanger(message=f"Flaskavel HTTP Runtime Exception: {error} detail: {traceback_list_errors[-1]}")
        return Response.flaskavelError(errors=traceback_list_errors, message=error)

    def handle_not_found(self, error):
        """
        Handles 404 errors with a custom response.

        Args:
            error: The 404 error encountered.

        Returns:
            Response: Custom not found response.
        """
        return Response.notFound()

    def run(self, host: str | None = None, port: int | None = None, debug: bool | None = None, load_dotenv: bool = True, **options: t.Any) -> None:
        """
        Starts the Flaskavel application server with custom configurations and console messages.

        Args:
            host (str, optional): Host address for the server. Defaults to None.
            port (int, optional): Port number for the server. Defaults to None.
            debug (bool, optional): Enable/disable debug mode. Defaults to None.
            load_dotenv (bool): Load .env file settings. Defaults to True.
            **options: Additional options for running the server.
        """
        if debug is not None:
            self.debug = bool(debug)

        # Retrieve the server name from configuration, if set.
        server_name = self.config.get("SERVER_NAME")
        sn_host = sn_port = None

        if server_name:
            sn_host, _, sn_port = server_name.partition(":")

        # Determine host and port values based on provided or default configurations.
        if not host:
            host = sn_host if sn_host else "127.0.0.1"
        if port or port == 0:
            port = int(port)
        elif sn_port:
            port = int(sn_port)
        else:
            port = 5000

        # Set default options for reloader, debugger, and threading.
        options.setdefault("use_reloader", self.debug)
        options.setdefault("use_debugger", self.debug)
        options.setdefault("threaded", True)

        # Output startup messages to the console.
        Console.clear()
        Console.textSuccess(" * Flaskavel App Started")
        if options['use_reloader']:
            Console.line(f" * Running on http://{host}:{port}")
            Console.textDanger(" * This is a development server. Do not use it in a production deployment.")

        # Run the server with Werkzeug's run_simple function.
        from werkzeug.serving import run_simple
        try:
            run_simple(t.cast(str, host), port, self, **options)
        finally:
            self._got_first_request = False
