import re
import importlib
import time
import traceback
import threading
import typing as t
from flask import Flask, request
from flask_cors import CORS
from flaskavel.lab.catalyst.config import Config
from flaskavel.lab.reagents.request import Request
from flaskavel.lab.beaker.console.output import Console
from flaskavel.lab.catalyst.bootstrap_cache import _BootstrapCache

class Flaskavel(Flask):

    def __init__(self, *args, **kwargs):
        super(Flaskavel, self).__init__(*args, **kwargs)
        self.register_error_handler(Exception, self.handle_global_error)
        self.start_time = time.time()

    def handle_global_error(self, e):
        error = str(e)
        traceback_list = traceback.format_tb(e.__traceback__)
        last_traceback_line_string = re.sub(r'\s+', ' ', traceback_list[-1].strip().replace('\n', ', '))
        Console.error(
            message=f"Flaskavel HTTP Runtime Exception: {error} detail: {last_traceback_line_string}",
            timestamp=True
        )
        exit(1)

    def run(
        self,
        host: str | None = None,
        port: int | None = None,
        debug: bool | None = None,
        load_dotenv: bool = True,
        **options: t.Any,
    ) -> None:

        if debug is not None:
            self.debug = bool(debug)

        server_name = self.config.get("SERVER_NAME")
        sn_host = sn_port = None

        if server_name:
            sn_host, _, sn_port = server_name.partition(":")

        if not host:
            if sn_host:
                host = sn_host
            else:
                host = "127.0.0.1"

        if port or port == 0:
            port = int(port)
        elif sn_port:
            port = int(sn_port)
        else:
            port = 5000

        options.setdefault("use_reloader", self.debug)
        options.setdefault("use_debugger", self.debug)
        options.setdefault("threaded", True)

        execution_duration = int((time.time() - self.start_time) * 1000)

        Console.clear()
        Console.executeTimestamp(
            command="FLASKAVEL APP STARTED 🚀 ",
            seconds=f"{execution_duration}ms",
            state='DONE'
        )

        from werkzeug.serving import run_simple
        try:
            run_simple(t.cast(str, host), port, self, **options)
        finally:
            self._got_first_request = False

class Kernel:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Kernel, cls).__new__(cls)
                cls._instance.app = Flaskavel(__name__)
                cls._instance.configure_app()
        return cls._instance

    def configure_app(self):
        app_config = Config.session()
        self.app.config.update({
            'PERMANENT_SESSION_LIFETIME': app_config['lifetime'],
            'SESSION_PERMANENT': app_config['expire_on_close'],
            'SESSION_USE_SIGNER': app_config['encrypt'],
            'SESSION_COOKIE_PATH': app_config['files'],
            'SESSION_COOKIE_NAME': app_config['cookie']['name'],
            'SESSION_COOKIE_DOMAIN': app_config['cookie']['domain'],
            'SESSION_COOKIE_SECURE': app_config['cookie']['secure'],
            'SESSION_COOKIE_HTTPONLY': app_config['cookie']['http_only'],
            'SESSION_COOKIE_SAMESITE': app_config['cookie']['same_site'],
            'SECRET_KEY': Config.app('key')
        })

        app_cors = Config.cors()
        CORS(
            app=self.app,
            methods=app_cors['allowed_methods'],
            origins=app_cors['allowed_origins'],
            allow_headers=app_cors['allowed_headers'],
            expose_headers=app_cors['exposed_headers'],
            max_age=app_cors['max_age']
        )

        routes = _BootstrapCache().get_routes()
        self.register_routes(routes)

    @staticmethod
    def load_module(module_path, classname):
        module = importlib.import_module(module_path)
        return getattr(module, classname)

    def apply_middlewares(self, controller_method, middlewares):
        if not middlewares:
            return controller_method

        def wrapped_controller(*args, **kwargs):
            next_func = controller_method
            for middleware in reversed(middlewares):
                middleware_class = self.load_module(middleware['module'], middleware['classname'])
                middleware_instance = middleware_class()

                # Sobreescribimos next_func para que pase por cada middleware
                def next_func_wrapper(next_func=next_func):
                    return middleware_instance.handle(Request(request=request), next_func, *args, **kwargs)
                next_func = next_func_wrapper

            return next_func()

        return wrapped_controller

    def register_routes(self, routes):
        for route in routes:
            controller_info = route['controller']
            middlewares = route.get('middlewares', [])

            # Cargar el método del controlador dinámicamente
            controller_class = self.load_module(controller_info['module_path'], controller_info['classname'])
            controller_instance = controller_class()
            controller_method = getattr(controller_instance, controller_info['method'])

            # Aplicar middlewares (si los hay) a la función del controlador
            wrapped_view_func = self.apply_middlewares(controller_method, middlewares)

            # Registrar la ruta en Flask
            self.app.add_url_rule(
                rule=route['uri'],
                endpoint=route['name'],
                view_func=wrapped_view_func,
                methods=[route['verb']]
            )

    def handle(self, *args, **kwargs):
        """Sobrescribir el método run para incluir el banner personalizado."""
        self.app.run(*args, **kwargs)
