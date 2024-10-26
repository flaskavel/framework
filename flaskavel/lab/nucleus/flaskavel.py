import re
import time
import traceback
import typing as t
from flask import Flask
from flaskavel.lab.reagents.response import Response, DumpExecution
from flaskavel.lab.beaker.console.output import Console

class Flaskavel(Flask):

    def __init__(self, *args, **kwargs):
        super(Flaskavel, self).__init__(*args, **kwargs)
        self.register_error_handler(Exception, self.handle_global_error)
        self.register_error_handler(404, self.handle_not_found)
        self.start_time = time.time()

    def handle_global_error(self, e):

        if isinstance(e, DumpExecution):
            return Response.dd(e.response)

        error = str(e)
        traceback_list = traceback.format_tb(e.__traceback__)

        traceback_list_errors = []
        for trace in traceback_list:
            if '\\flask\\' not in trace and '\\werkzeug\\' not in trace:
                traceback_list_errors.append((re.sub(r'\s+', ' ', trace.strip().replace('\n', ' - ').replace('^', ' '))).strip(' - '))

        Console.error(message=f"Flaskavel HTTP Runtime Exception: {error} detail: {traceback_list_errors[-1]}", timestamp=True)
        return Response.flaskavelError(errros=traceback_list_errors, message=error)

    def handle_not_found(self, error):
        return Response.notFound()

    def run(self, host: str | None = None, port: int | None = None, debug: bool | None = None, load_dotenv: bool = True, **options: t.Any) -> None:

        if debug is not None:
            self.debug = bool(debug)

        server_name = self.config.get("SERVER_NAME")
        sn_host = sn_port = None

        if server_name:
            sn_host, _, sn_port = server_name.partition(":")

        if not host:
            host = sn_host if sn_host else "127.0.0.1"

        if port or port == 0:
            port = int(port)
        elif sn_port:
            port = int(sn_port)
        else:
            port = 5000

        options.setdefault("use_reloader", self.debug)
        options.setdefault("use_debugger", self.debug)
        options.setdefault("threaded", True)

        Console.clear()
        Console.textSuccess(f" * Flaskavel App Started")
        if(options['use_reloader']):
            Console.line(f" * Running on http://{host}:{port}")
            Console.textDanger(f" * This is a development server. Do not use it in a production deployment.")

        from werkzeug.serving import run_simple
        try:
            run_simple(t.cast(str, host), port, self, **options)
        finally:
            self._got_first_request = False