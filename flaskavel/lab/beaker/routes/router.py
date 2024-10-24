from flaskavel.lab.catalyst.router_instances import _RouteInstances

class Route:
    """
    A class that provides a static interface for managing routing in Flaskavel.
    It interacts with the singleton _RouteInstances to handle route configurations.
    """

    @staticmethod
    def middleware(middleware: list = []) -> 'RouteHandle':
        """
        Set middleware for a route.

        Args:
            middleware (list): List of middleware to apply.

        Returns:
            RouteHandle: The route handler with the middleware set.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().middleware(middleware=middleware))
        return routes.route_instances[-1]

    @staticmethod
    def prefix(prefix: str) -> 'RouteHandle':
        """
        Set a prefix for a route.

        Args:
            prefix (str): The prefix to apply to the route.

        Returns:
            RouteHandle: The route handler with the prefix set.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().prefix(prefix=prefix))
        return routes.route_instances[-1]

    @staticmethod
    def controller(classname: str) -> 'RouteHandle':
        """
        Set the controller for a route.

        Args:
            classname (str): The name of the controller class.

        Returns:
            RouteHandle: The route handler with the controller set.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().controller(classname=classname))
        return routes.route_instances[-1]

    @staticmethod
    def module(module: str) -> 'RouteHandle':
        """
        Set the module for a route.

        Args:
            module (str): The module to apply to the route.

        Returns:
            RouteHandle: The route handler with the module set.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().module(module=module))
        return routes.route_instances[-1]

    @staticmethod
    def group(*args) -> 'RouteHandle':
        """
        Group multiple route configurations together.

        Args:
            *args: The RouteHandle instances to group.

        Returns:
            RouteHandle: The route handler representing the group.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().group(*args))
        return routes.route_instances[-1]

    @staticmethod
    def name(name: str) -> 'RouteHandle':
        """
        Set a name for the route.

        Args:
            name (str): The name of the route.

        Returns:
            RouteHandle: The route handler with the name set.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().name(name=name))
        return routes.route_instances[-1]

    @staticmethod
    def get(uri: str, method: str = None) -> 'RouteHandle':
        """
        Define a GET route.

        Args:
            uri (str): The URI pattern for the GET route.
            method (str, optional): The method to handle the GET request.

        Returns:
            RouteHandle: The route handler for the GET request.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().get(uri=uri, method=method))
        return routes.route_instances[-1]

    @staticmethod
    def post(uri: str, method: str = None) -> 'RouteHandle':
        """
        Define a POST route.

        Args:
            uri (str): The URI pattern for the POST route.
            method (str, optional): The method to handle the POST request.

        Returns:
            RouteHandle: The route handler for the POST request.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().post(uri=uri, method=method))
        return routes.route_instances[-1]

    @staticmethod
    def put(uri: str, method: str = None) -> 'RouteHandle':
        """
        Define a PUT route.

        Args:
            uri (str): The URI pattern for the PUT route.
            method (str, optional): The method to handle the PUT request.

        Returns:
            RouteHandle: The route handler for the PUT request.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().put(uri=uri, method=method))
        return routes.route_instances[-1]

    @staticmethod
    def patch(uri: str, method: str = None) -> 'RouteHandle':
        """
        Define a PATCH route.

        Args:
            uri (str): The URI pattern for the PATCH route.
            method (str, optional): The method to handle the PATCH request.

        Returns:
            RouteHandle: The route handler for the PATCH request.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().patch(uri=uri, method=method))
        return routes.route_instances[-1]

    @staticmethod
    def delete(uri: str, method: str = None) -> 'RouteHandle':
        """
        Define a DELETE route.

        Args:
            uri (str): The URI pattern for the DELETE route.
            method (str, optional): The method to handle the DELETE request.

        Returns:
            RouteHandle: The route handler for the DELETE request.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().delete(uri=uri, method=method))
        return routes.route_instances[-1]

    @staticmethod
    def options(uri: str, method: str = None) -> 'RouteHandle':
        """
        Define an OPTIONS route.

        Args:
            uri (str): The URI pattern for the OPTIONS route.
            method (str, optional): The method to handle the OPTIONS request.

        Returns:
            RouteHandle: The route handler for the OPTIONS request.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().options(uri=uri, method=method))
        return routes.route_instances[-1]

    @staticmethod
    def action(action: str) -> 'RouteHandle':
        """
        Set the action handler for the route.

        Args:
            action (str): The action handler method.

        Returns:
            RouteHandle: The route handler with the action set.
        """
        routes = _RouteInstances()
        routes.add_instance(RouteHandle().action(action=action))
        return routes.route_instances[-1]


class RouteHandle:
    """
    A class that handles individual route configurations, including HTTP methods, URIs,
    middleware, controllers, and more.
    """

    def __init__(self):
        self._middleware = None
        self._prefix = None
        self._controller = None
        self._module = None
        self._verb = None
        self._method = None
        self._name = None
        self._uri = None
        self._type = None

    def middleware(self, middleware: list = []):
        """Set middleware for the route."""
        self._middleware = middleware
        return self

    def prefix(self, prefix: str):
        """Set a prefix for the route URI."""
        self._prefix = self._clean_prefix(prefix)
        return self

    def controller(self, classname: str):
        """Set the controller class name for the route."""
        self._controller = classname
        return self

    def module(self, module: str):
        """Set the module for the route."""
        self._module = module
        return self

    def group(self, *args):
        """
        Group multiple route configurations together.
        This method ensures shared properties like middleware, prefixes, and more.
        """
        instances = _RouteInstances()
        instances.route_instances.remove(self)

        for instance in args:
            if not instance._middleware:
                instance._middleware = self._middleware
            if not instance._prefix:
                instance._prefix = self._prefix
            if not instance._controller:
                instance._controller = self._controller
            if not instance._module:
                instance._module = self._module or self._controller
            if not instance._verb:
                instance._verb = self._verb
            if not instance._method:
                instance._method = self._method
            if not instance._name:
                instance._name = self._name
            if not instance._uri:
                instance._uri = self._uri

        return self

    def name(self, name: str):
        """Set the name of the route."""
        self._name = name
        return self

    def get(self, uri: str, method: str = None):
        """Define a GET request handler for the route."""
        self._uri = self._clean_uri(uri)
        self._verb = 'GET'
        self._method = method
        return self

    def post(self, uri: str, method: str = None):
        """Define a POST request handler for the route."""
        self._uri = self._clean_uri(uri)
        self._verb = 'POST'
        self._method = method
        return self

    def put(self, uri: str, method: str = None):
        """Define a PUT request handler for the route."""
        self._uri = self._clean_uri(uri)
        self._verb = 'PUT'
        self._method = method
        return self

    def patch(self, uri: str, method: str = None):
        """Define a PATCH request handler for the route."""
        self._uri = self._clean_uri(uri)
        self._verb = 'PATCH'
        self._method = method
        return self

    def delete(self, uri: str, method: str = None):
        """Define a DELETE request handler for the route."""
        self._uri = self._clean_uri(uri)
        self._verb = 'DELETE'
        self._method = method
        return self

    def options(self, uri: str, method: str = None):
        """Define an OPTIONS request handler for the route."""
        self._uri = self._clean_uri(uri)
        self._verb = 'OPTIONS'
        self._method = method
        return self

    def action(self, action: str):
        """Set the action for the route."""
        self._method = action
        return self

    def _clean_prefix(self, prefix: str) -> str:
        """
        Cleans the given prefix by checking for invalid characters and standardizing its format.

        Args:
            prefix (str): The prefix string to be cleaned.

        Returns:
            str: The cleaned prefix.

        Raises:
            ValueError: If the prefix contains any of the forbidden characters.
        """
        # List of forbidden characters
        forbidden_chars = ['<', '>', '{', '}']

        # Check for forbidden characters in the prefix
        for char in forbidden_chars:
            if char in prefix:
                raise ValueError(f"The character '{char}' is not allowed in the prefix.")

        # Replace double slashes with a single slash
        prefix = prefix.replace('//', '/')

        # Remove the leading slash if it exists
        if not prefix.startswith('/'):
            prefix = f"/{prefix}"

        # Remove the trailing slash if it exists and the length is greater than 1
        if prefix.endswith('/') and len(prefix) > 1:
            prefix = prefix[:-1]

        return prefix

    def _clean_uri(self, uri: str) -> str:
        """
        Cleans the given URI by standardizing its format. This includes replacing curly braces
        with angle brackets, removing extra slashes, and ensuring the URI starts and ends correctly.

        Args:
            uri (str): The URI string to be cleaned.

        Returns:
            str: The cleaned URI.
        """
        # Replace curly braces with angle brackets and remove unnecessary spaces
        uri = str(uri).replace('{', '<').replace('}', '>').strip()

        # Replace double slashes with a single slash
        uri = uri.replace('//', '/')

        # Ensure the URI starts with a single slash
        if not uri.startswith('/'):
            uri = f"/{uri}"

        # Remove the trailing slash if it exists (except for the root '/')
        if uri.endswith('/') and len(uri) > 1:
            uri = uri[:-1]

        return uri
