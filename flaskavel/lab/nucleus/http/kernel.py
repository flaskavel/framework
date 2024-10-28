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
        """Ensure that only one instance of Kernel is created (Singleton pattern)."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Kernel, cls).__new__(cls)
                cls._instance.app = Flaskavel(__name__)
                cls._instance.configure_app()
        return cls._instance

    def configure_app(self):
        """Configure the Flaskavel application with session, CORS, and route settings."""
        app_config = Config.session()
        # Set session configurations based on Config values
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

        # Configure CORS for the application
        app_cors = Config.cors()
        CORS(
            app=self.app,
            methods=app_cors['allowed_methods'],
            origins=app_cors['allowed_origins'],
            allow_headers=app_cors['allowed_headers'],
            expose_headers=app_cors['exposed_headers'],
            max_age=app_cors['max_age']
        )

        # Register application routes
        routes = _BootstrapCache().get_routes()
        self.register_routes(routes)

    @staticmethod
    def load_module(module_path, classname):
        """Dynamically import a module and retrieve the specified class."""
        module = importlib.import_module(module_path)
        return getattr(module, classname)

    def apply_middlewares(self, controller_method, middlewares):
        """Apply middleware to a controller method, if any middlewares are provided."""
        # Return the controller method directly if no middlewares exist
        if not middlewares:
            return controller_method

        # Define a recursive function to wrap each middleware
        def wrap_with_middleware(index, **kwargs):
            # If all middlewares have been applied, call the controller method
            if index >= len(middlewares):
                return controller_method(**kwargs)

            # Load the current middleware
            middleware_info = middlewares[index]
            middleware_class = self.load_module(middleware_info['module'], middleware_info['classname'])
            middleware_instance = middleware_class()

            # Call the next middleware by wrapping it with `wrap_with_middleware`
            return middleware_instance.handle(
                lambda: wrap_with_middleware(index + 1, **kwargs),
                **kwargs
            )

        # Start with the first middleware (index 0)
        return lambda **kwargs: wrap_with_middleware(0, **kwargs)

    def register_routes(self, routes):
        """Register routes dynamically using specified controllers and middlewares."""
        for route in routes:
            controller_info = route['controller']
            middlewares = route.get('middlewares', [])

            # Dynamically load the controller
            controller_class = self.load_module(controller_info['module_path'], controller_info['classname'])
            controller_instance = controller_class()
            controller_method = getattr(controller_instance, controller_info['method'])

            # Apply middlewares to the controller method
            wrapped_view_func = self.apply_middlewares(controller_method, middlewares)

            # Register the route in Flask
            self.app.add_url_rule(
                rule=route['uri'],
                endpoint=route['name'],
                view_func=wrapped_view_func,
                methods=[route['verb']]
            )

    def handle(self, *args, **kwargs):
        """Override the run method to include a custom banner when starting the app."""
        self.app.run(*args, **kwargs)
