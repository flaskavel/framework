import importlib
import threading
from flask_cors import CORS
from flaskavel.lab.catalyst.config import Config
from flaskavel.lab.nucleus.flaskavel import Flaskavel
from flaskavel.lab.catalyst.bootstrap_cache import _BootstrapCache

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
        # Si no hay middlewares, devolvemos el controlador directamente
        if not middlewares:
            return controller_method

        # Definir una función recursiva que encadene los middlewares
        def wrap_with_middleware(index, **kwargs):
            # Si hemos pasado por todos los middlewares, llamamos al controlador
            if index >= len(middlewares):
                return controller_method(**kwargs)

            # Cargar el middleware actual
            middleware_info = middlewares[index]
            middleware_class = self.load_module(middleware_info['module'], middleware_info['classname'])
            middleware_instance = middleware_class()

            # Llamar el siguiente middleware pasando `wrap_with_middleware` con el siguiente índice
            return middleware_instance.handle(
                lambda: wrap_with_middleware(index + 1, **kwargs),
                **kwargs
            )

        # Empezamos con el primer middleware (índice 0)
        return lambda **kwargs: wrap_with_middleware(0, **kwargs)

    def register_routes(self, routes):
        for route in routes:
            controller_info = route['controller']
            middlewares = route.get('middlewares', [])

            # Cargar dinámicamente el controlador
            controller_class = self.load_module(controller_info['module_path'], controller_info['classname'])
            controller_instance = controller_class()
            controller_method = getattr(controller_instance, controller_info['method'])

            # Aplicar los middlewares al controlador
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

