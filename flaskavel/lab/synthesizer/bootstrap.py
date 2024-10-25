import os
import sys
import time
import importlib
from pathlib import Path
from flaskavel.lab.reagents.crypt import Crypt
from flaskavel.lab.catalyst.paths import _Paths
from flaskavel.lab.beaker.console.output import Console
from flaskavel.lab.synthesizer.cache import FlaskavelCache
from flaskavel.lab.catalyst.environment import _Environment
from flaskavel.lab.catalyst.router_instances import _RouteInstances
from flaskavel.lab.synthesizer.runner import FlaskavelRunner

class FlaskavelBootstrap:
    """Handles the bootstrapping of the Flaskavel application."""

    def __init__(self, basePath:Path):
        """Initialize FlaskavelBootstrap with the base path.

        Args:
            basePath: The base path for the application.
        """
        self.start_time = time.time()
        self.base_path = basePath

        self.cache = FlaskavelCache(basePath=self.base_path)
        self.started = self.cache.validate()

        self.dict_config = {}
        self.file_config = None
        self.dict_routes = {}
        self.file_routes = None
        self.encrypt = False

    def withRouting(self, api: list = [], web: list = []):
        """Define API and web routes for the application.

        Args:
            api (list): List of API routes.
            web (list): List of web routes.

        Returns:
            FlaskavelBootstrap: The current instance of FlaskavelBootstrap.
        """
        if not self.started:
            self.apiRoutes = api
            self.webRoutes = web

        return self

    def withMiddlewares(self, aliases: dict = {}, use: list = []):
        """Define middleware configurations.

        Args:
            aliases (dict): Middleware aliases.
            use (list): Middleware to use.

        Returns:
            FlaskavelBootstrap: The current instance of FlaskavelBootstrap.
        """
        if not self.started:
            self.aliasesMiddleware = aliases
            self.useMiddleware = use
        return self

    def create(self):
        """Create and initialize the application.

        Returns:
            FlaskavelRunner: An instance of FlaskavelRunner if the application is created successfully.
        """
        try:
            if not self.started:

                self.cache.clearStart()
                _Environment(path=os.path.join(self.base_path, '.env'))
                _Paths(path=self.base_path)
                self._update_path()
                self._files()
                self._config()
                self._middlewares()
                self._routes()
                self._cache()
                self.cache.register(
                    path_cache_config=self.file_config,
                    path_cache_routes=self.file_routes,
                    encrypt=self.encrypt,
                    key=self.app_key
                )

                execution_duration = int((time.time() - self.start_time) * 1000)
                Console.info(message=f"Bootstrapping Flaskavel - {execution_duration}ms", timestamp=True)

            self.cache.mount()
            return FlaskavelRunner(basePath=self.base_path, start_time=self.start_time)

        except Exception as e:
            Console.error(message=f"Critical Bootstrap Error in Flaskavel: {e}", timestamp=True)
            raise ValueError(e)

    def _middlewares(self):
        """Load and validate middlewares for aliases and used middleware."""

        # Initialize the dictionaries for middlewares
        aliasesMiddleware = {}

        # Iterate over the alias-based middlewares
        for alias, details in self.aliasesMiddleware.items():
            module_path = f"app.Http.Middlewares.{details['module']}"

            # Import the module and validate the middleware class and method
            try:
                module = __import__(module_path, fromlist=[details["classname"]])
            except ImportError:
                raise ImportError(
                    f"Module '{module_path}' for middleware alias '{alias}' does not exist in 'aliasesMiddleware:aliases'."
                )

            # Check if the middleware class exists in the module
            middleware_class = getattr(module, details["classname"], None)
            if not middleware_class:
                raise ImportError(
                    f"Middleware class '{details['classname']}' for alias '{alias}' not found in module '{module_path}'."
                )

            # Check if the 'handle' method exists in the middleware class
            if not hasattr(middleware_class, 'handle'):
                raise AttributeError(
                    f"The 'handle' method is required in the middleware class '{details['classname']}' for alias '{alias}'."
                )

            # Add the middleware to the aliasesMiddleware dictionary
            aliasesMiddleware[alias] = {
                'module': module_path,
                'classname': details['classname'],
                'method': 'handle',
            }

        # Update the class attribute with the validated aliases middleware
        self.aliasesMiddleware = aliasesMiddleware

        # Initialize the dictionary for useMiddleware
        useMiddleware = []

        # Iterate over the globally used middlewares
        for middleware in self.useMiddleware:
            module_path = f"app.Http.Middlewares.{middleware['module']}"

            # Import the module and validate the middleware class and method
            try:
                module = __import__(module_path, fromlist=[middleware["classname"]])
            except ImportError:
                raise ImportError(
                    f"Module '{module_path}' does not exist in 'withMiddlewares:use'."
                )

            # Check if the middleware class exists in the module
            middleware_class = getattr(module, middleware["classname"], None)
            if not middleware_class:
                raise ImportError(
                    f"Middleware class '{middleware['classname']}' not found in module '{module_path}'."
                )

            # Check if the 'handle' method exists in the middleware class
            if not hasattr(middleware_class, 'handle'):
                raise AttributeError(
                    f"The 'handle' method is required in the middleware class '{middleware['classname']}'."
                )

            # Add the middleware to the useMiddleware dictionary
            useMiddleware.append({
                'module': module_path,
                'classname': middleware['classname'],
                'method': 'handle',
            })

        # Update the class attribute with the validated used middleware
        self.useMiddleware = useMiddleware

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

        if self.base_path not in sys.path:
            sys.path.append(self.base_path)

        for folder in paths:
            for root, dirs, files in os.walk(os.path.join(self.base_path, folder)):
                if os.path.isdir(root) and root not in sys.path:
                    sys.path.append(root)

    def _files(self):
        """Load application configuration from config files."""
        from config.cache import cache # type: ignore

        # Determina si se debe encriptar.
        self.encrypt = cache['encrypt']

        # Determina el almacenamiento del cache (por el momento file)
        store = cache['default']

        # Determina la ruta de guardado del cache de configuración
        self.file_config = cache['store'][store]['config']
        self.file_routes = cache['store'][store]['routes']

    def _config(self):

        # Modules
        from config.app import app # type: ignore
        from config.auth import auth # type: ignore
        from config.cors import cors # type: ignore
        from config.database import database # type: ignore
        from config.filesystems import filesystems # type: ignore
        from config.logging import logging # type: ignore
        from config.mail import mail # type: ignore
        from config.queue import queue # type: ignore
        from config.session import session # type: ignore

        # Get App Key
        self.app_key = app['key']

        # Data Bootstrap
        bootstrap = {
            'time' : str(time.time()),
            'base_path' : str(self.base_path),
            'cache' : {
                'config' : self.file_config,
                'routes' : self.file_routes,
            }
        }

        # String Configuration
        self.dict_config = f"{{'app':{app},'auth':{auth},'cors':{cors},'database':{database},'filesystems':{filesystems},'logging':{logging},'mail':{mail},'queue': {queue},'session':{session},'bootstrap':{bootstrap}}}"

    def _routes(self):
        """Load and validate application routes."""

        # Mount the Singleton instance for routes
        routes = _RouteInstances()

        # Load and execute route files dynamically
        for file in self.apiRoutes + self.webRoutes:
            importlib.import_module(f"routes.{file}")

        # Retrieve all generated routes
        all_routes = routes.get_routes()

        # Ensure route integrity and validate each route
        required_fields = ['controller', 'module', 'method', 'verb', 'uri']

        for route in all_routes:

            # Check for required fields in each route
            for field in required_fields:
                if not route.get(field):
                    raise ValueError(f"Missing required value for '{field}' in route: {str(route)}")

            # Check for duplicate route names
            if route.get("name"):
                duplicate_name = next((_r for _r in all_routes if _r["name"] == route["name"] and _r is not route), None)
                if duplicate_name:
                    raise ValueError(f"Route name '{route['name']}' is already in use by another route: {duplicate_name}")

        # Check for duplicate URIs with the same HTTP verb and prefix
        for route in all_routes:
            for _route in all_routes:
                if (_route is not route and
                    route["uri"] == _route["uri"] and
                    route["prefix"] == _route["prefix"] and
                    route["verb"] == _route["verb"]):
                    raise ValueError(f"URI '{route['uri']}' with prefix '{route['prefix']}' "
                                    f"and verb '{route['verb']}' is already in use by another route: {_route}")

            # Import the module and validate the controller and method
            try:
                module = __import__(route["module"], fromlist=[route["controller"]])
            except ImportError:
                raise ImportError(f"Module '{route['module']}' does not exist for route: {route}")

            controller_class = getattr(module, route["controller"], None)
            if not controller_class:
                raise ImportError(f"Controller class '{route['controller']}' not found in module '{route['module']}' for route: {route}")

            # Check if the method exists in the controller
            if not hasattr(controller_class, route["method"]):
                raise AttributeError(f"Method '{route['method']}' not found in controller '{route['controller']}' for route: {route}")

        # Validate Middlewares in routes
        for route in all_routes:
            middlewares = route.get("middleware", [])
            if isinstance(middlewares, list):
                for middleware in middlewares:
                    if middleware not in self.aliasesMiddleware:
                        raise KeyError(f"The middleware with alias '{middleware}' does not exist in 'aliasesMiddleware'.")

        real_routes = []
        for route in all_routes:

            # Create a copy to avoid modifying the original list
            route_middleware = self.useMiddleware.copy()

            # Iterate through each middleware defined in the route
            for single_middleware in route['middleware']:

                # Append the corresponding middleware configuration to the list
                route_middleware.append(self.aliasesMiddleware[single_middleware])

            # Remove duplicates from the list of middlewares
            unique_data = [dict(item) for item in {frozenset(item.items()): item for item in route_middleware}.values()]

            # Create Data Route
            single_route = {
                'controller' : {
                    'module_path' : str(route['module']).strip(),
                    'classname' : str(route['controller']).strip(),
                    'method' : str(route['method']).strip()
                },
                'middlewares' : unique_data,
                'uri' : str(f"{route['prefix']}{route['uri']}").replace('//','/').strip(),
                'verb' : str(route['verb']).upper().strip(),
                'name' : str(route['name']).strip(),
            }

            # Add Pool Routes
            real_routes.append(single_route)

        # Convert routes to string for storage or further use
        self.dict_routes = real_routes

    def _cache(self):
        """Cache the configuration and routes in encrypted or plain format."""

        if self.encrypt:
            config_content = Crypt.encrypt(value=str(self.dict_config), key=self.app_key)
            routes_content = Crypt.encrypt(value=str(self.dict_routes), key=self.app_key)
        else:
            config_content = str(self.dict_config)
            routes_content = str(self.dict_routes)

        all_data = [
            {'file' : self.file_config, 'content' : config_content},
            {'file' : self.file_routes, 'content' : routes_content}
        ]

        for data in all_data:
            if os.path.exists(data['file']):
                os.remove(data['file'])
            with open(data['file'], 'wb') as file_cache_config:
                file_cache_config.write(str(data['content']).encode())
