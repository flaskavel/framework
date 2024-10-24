import threading
import inspect

class _RouteInstances:
    """
    A thread-safe singleton class to manage route instances.
    """

    # Singleton instance and lock for thread safety
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        Creates a new instance of the RouteInstances class if it does not already exist.
        Ensures thread safety using a lock to prevent race conditions.

        :return: The singleton instance of the RouteInstances class.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(_RouteInstances, cls).__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initializes the instance attributes. This is only called once during the
        first creation of the singleton instance.
        """
        self.route_instances = []

    def add_instance(self, instance):
        """
        Adds a new route instance to the list, ensuring that there are no name or
        URI conflicts with existing routes.

        :param instance: The instance to add to the route_instances list.
        :raises ValueError: If the route name or URI with the same HTTP verb already exists.
        """
        frame_info = inspect.stack()[2]
        origin = str(frame_info.filename).split('\\')
        origin = origin[-1].replace('.py','').strip()
        instance._type = origin

        self.route_instances.append(instance)

    def get_routes(self):
        """
        Returns a list of all route instances as dictionaries for easier processing.

        :return: A list of dictionaries representing route instances.
        """
        routes = []
        for route in self.route_instances:

            if route._type == 'api':
                if route._prefix:
                    route._prefix = f"/api{route._prefix}"
                else:
                    route._prefix = f"/api"

            name = route._name if route._name else (route._prefix + route._uri).replace('/', '.')
            name = name.strip('.')

            routes.append({
                'middleware': route._middleware,
                'prefix': route._prefix,
                'controller': route._controller,
                'module': f"app.Http.Controllers.{route._module if route._module else route._controller}",
                'verb': route._verb,
                'method': route._method,
                'name': name,
                'uri': route._uri
            })

        return routes
