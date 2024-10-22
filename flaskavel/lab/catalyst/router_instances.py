import threading

class _RouteInstances:

    # Singleton instance and lock for thread safety
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        Creates a new instance of the _RouteInstances class if it does not already exist.
        Ensures thread safety using a lock to prevent race conditions.

        :return: The singleton instance of the _RouteInstances class.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(_RouteInstances, cls).__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self): 
        """
        Initializes instance attributes.
        Called only once during the first creation of the singleton instance.
        """
        self.classInstances = []

    def setInstance(self, instance):
        """
        Adds a new instance to the list of class instances.

        :param instance: The instance to add to the classInstances list.
        """
        self.classInstances.append(instance)

    def getDict(self):

        routes = []
        for route in self.classInstances:
            routes.append({
                'middleware' : route._middleware,
                'prefix' : route._prefix,
                'controller' : route._controller,
                'controller' : route._controller,
                'module' : route._module,
                'verb' : route._verb,
                'method' : route._method,
                'name' : route._name,
                'uri' : route._uri
            })