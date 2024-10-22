import os
import sys
import time
import json
import tempfile
import importlib
from pathlib import WindowsPath
from flaskavel.lab.reagents.crypt import Crypt
from flaskavel.lab.catalyst.paths import _Paths
from flaskavel.lab.atomic.environment import Env
from flaskavel.lab.beaker.console.output import Console
from flaskavel.lab.catalyst.environment import _Environment
from flaskavel.lab.catalyst.router_instances import _RouteInstances

class Application:
    """Application class to configure the Flaskavel framework."""

    @staticmethod
    def configure(base_path: WindowsPath):
        """Configure the Flaskavel framework with the given base path.

        Args:
            base_path (WindowsPath): The base path for the application.

        Returns:
            FlaskavelBootstrap: An instance of FlaskavelBootstrap configured with the base path.
        """
        return FlaskavelBootstrap(basePath=base_path)

class FlaskavelCache:
    """Handles caching mechanisms for the Flaskavel application."""

    def __init__(self, basePath: WindowsPath):
        """Initialize FlaskavelCache with the base path.

        Args:
            basePath (WindowsPath): The base path for the application.
        """
        self.basePath = basePath
        self.started_file = 'started.lab'

    def clearStart(self):
        """Clear the cache for the started file, if it exists."""
        started_file = os.path.join(tempfile.gettempdir(), self.started_file)
        if os.path.exists(started_file):
            os.remove(started_file)

    def validate(self):
        """Validate the cache based on the existence of the started file and its timestamp.

        Returns:
            bool: True if the cache is valid, False otherwise.
        """
        started_file = os.path.join(tempfile.gettempdir(), self.started_file)
        if not os.path.exists(started_file):
            return False

        with open(started_file, 'r') as file:
            data_file = file.read()
        start_time = Crypt.decrypt(value=data_file)

        env_path = os.path.join(self.basePath, '.env')
        last_edit = os.path.getmtime(env_path)
        if float(last_edit) >= float(start_time):
            return False

        app_path = os.path.join(self.basePath, 'bootstrap', 'app.py')
        last_edit = os.path.getmtime(app_path)
        if float(last_edit) >= float(start_time):
            return False

        list_files = os.listdir(os.path.join(self.basePath, 'config'))
        for file in list_files:
            full_path = os.path.abspath(os.path.join(self.basePath, 'config', file))
            if os.path.isfile(full_path):
                if float(os.path.getmtime(full_path)) >= float(start_time):
                    return False

        return True

    def register(self, started_file: str = 'started.lab'):
        """Register the start time in the cache.

        Args:
            started_file (str): The name of the started file to create.
        """
        started_file = os.path.join(tempfile.gettempdir(), started_file)
        start_time = Crypt.encrypt(value=str(time.time()))
        with open(started_file, 'wb') as file:
            file.write(start_time.encode())

class FlaskavelBootstrap:
    """Handles the bootstrapping of the Flaskavel application."""

    def __init__(self, basePath):
        """Initialize FlaskavelBootstrap with the base path.

        Args:
            basePath: The base path for the application.
        """
        self.base_path = basePath
        self.cache = FlaskavelCache(basePath=self.base_path)
        self.dict_config = {}
        self.file_config = {}
        self.dict_routes = {}
        self.file_routes = {}
        self.encrypt = False

    def withRouting(self, api: tuple, web: tuple):
        """Define API and web routes for the application.

        Args:
            api (tuple): Tuple of API routes.
            web (tuple): Tuple of web routes.

        Returns:
            FlaskavelBootstrap: The current instance of FlaskavelBootstrap.
        """
        self.apiRoutes = api
        self.webRoutes = web
        return self

    def withMiddlewares(self, aliases: dict, use: dict):
        """Define middleware configurations.

        Args:
            aliases (dict): Middleware aliases.
            use (dict): Middleware to use.

        Returns:
            FlaskavelBootstrap: The current instance of FlaskavelBootstrap.
        """
        self.aliasesMiddleware = aliases
        self.useMiddleware = use
        return self

    def create(self):
        """Create and initialize the application.

        Returns:
            FlaskavelRunner: An instance of FlaskavelRunner if the application is created successfully.
        """
        try:
            if not self.cache.validate():
                self.cache.clearStart()

                _Environment(path=os.path.join(self.base_path, '.env'))
                _Paths(path=os.path.join(self.base_path))
                self._update_path()
                self._config()
                self._routes()
                self._cache()
                self.cache.register()

            return FlaskavelRunner(basePath=self.base_path)

        except Exception as e:

            Console.error(
                message=f"Critical Bootstrap Error in Flaskavel: {e}",
                timestamp=True
            )
            exit(1)

    def _update_path(self):
        """Update the system path to include application directories."""
        paths = [
            'app',
            'bootstrap',
            'config',
            'database',
            'public',
            'resources',
            'routes',
            'storage',
            'tests'
        ]

        for folder in paths:
            full_path = os.path.abspath(os.path.join(self.base_path, folder))
            if os.path.isdir(full_path) and full_path not in sys.path:
                sys.path.append(full_path)

    def _config(self):
        """Load application configuration from config files."""
        from config.cache import cache # type: ignore

        # Determina si se debe encriptar.
        self.encrypt = bool(cache['encrypt'])

        # Determina el almacenamiento del cache (por el momento file)
        store = cache['default']

        # Determina la ruta de guardado del cache de configuración
        self.file_config = cache['store'][store]['config']
        self.file_routes = cache['store'][store]['routes']

        from config.app import app # type: ignore
        from config.auth import auth # type: ignore
        from config.cors import cors # type: ignore
        from config.database import database # type: ignore
        from config.filesystems import filesystems # type: ignore
        from config.logging import logging # type: ignore
        from config.mail import mail # type: ignore
        from config.queue import queue # type: ignore
        from config.session import session # type: ignore

        self.dict_config = {
            'app': app,
            'auth': auth,
            'cors': cors,
            'database': database,
            'filesystems': filesystems,
            'logging': logging,
            'mail': mail,
            'queue': queue,
            'session': session
        }

    def _routes(self):
        """Load and validate application routes."""

        # Mount the Singleton instance for routes
        routes = _RouteInstances()

        # Load and execute route files
        for file in self.apiRoutes:
            importlib.import_module(f"routes.{file}")

        # Retrieve all generated routes
        all_routes = routes.get_routes()

        # Ensure route integrity
        for route in all_routes:

            # Check for required fields in each route
            required_fields = ['controller', 'module', 'method', 'verb', 'uri']
            for field in required_fields:
                if not route[field]:
                    raise ValueError(f"Missing required value for <{field}> in route.")

            # Check for duplicate route names
            if route["name"]:
                for _route in all_routes:
                    if _route['name'] == route["name"] and _route is not route:
                        raise ValueError(f"Route name is already in use: <{route['name']}>")

        for _route in all_routes:

            # Check for duplicate URIs with the same HTTP verb
            if (route["uri"] == _route["uri"] and
                route["prefix"] == _route["prefix"] and
                route["verb"] == _route["verb"] and _route is not route):
                raise ValueError(f"URI <{route['uri']}> with prefix <{route['prefix']}> and verb <{route['verb']}> is already in use.")

            try:
                module = __import__(route["module"], fromlist=[route["controller"]])
            except ImportError:
                raise ImportError(f"The module '{route['module']}' dont exist.")

            if not hasattr(module, route["controller"]):
                raise ImportError(f"The class '{route['controller']}' was not found in the module '{route['module']}'.")

            # Check if the class has the specified method
            new_class = getattr(module, route["controller"])
            if not hasattr(new_class, route["method"]):
                raise AttributeError(f"The method '{route['method']}' does not exist in the class '{route['controller']}'.")

        self.dict_routes = all_routes

    def _cache(self):
        """Cache the configuration and routes in encrypted or plain format."""

        if self.encrypt:
            app_key = Env.get('APP_KEY', None)
            config_content = Crypt.encrypt(
                value=json.dumps(self.dict_config),
                key=app_key
            )
            routes_content = Crypt.encrypt(
                value=json.dumps(self.dict_routes),
                key=app_key
            )
        else:
            config_content = json.dumps(self.dict_config)
            routes_content = json.dumps(self.dict_config)

        all_data = [
            {
                'file' : self.file_config,
                'content' : config_content
            },{
                'file' : self.file_routes,
                'content' : routes_content
            }
        ]

        for data in all_data:
            if os.path.exists(data['file']):
                os.remove(data['file'])
            with open(data['file'], 'wb') as file_cache_config:
                file_cache_config.write(data['content'].encode())

class FlaskavelRunner():
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