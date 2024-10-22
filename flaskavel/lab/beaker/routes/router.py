from flaskavel.lab.catalyst.router_instances import _RouteInstances

class Route:

    @staticmethod
    def middleware(middleware:list = []) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().middleware(middleware=middleware))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def prefix(prefix:str) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().prefix(prefix=prefix))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def controller(classname:str) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().controller(classname=classname))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def module(module:str) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().module(module=module))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def group(*args) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().group(*args))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def name(name:str) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().name(name=name))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def get(uri:str, method:str=None) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().get(uri=uri, method=method))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def post(uri:str, method:str=None) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().post(uri=uri, method=method))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def put(uri:str, method:str=None) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().put(uri=uri, method=method))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def patch(uri:str, method:str=None) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().patch(uri=uri, method=method))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def delete(uri:str, method:str=None) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().delete(uri=uri, method=method))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def options(uri:str, method:str=None) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().options(uri=uri, method=method))
        return routes.classInstances[len(routes.classInstances) - 1]

    @staticmethod
    def action(action:str) -> 'RouteHandle':
        routes = _RouteInstances()
        routes.setInstance(RouteHandle().action(action=action))
        return routes.classInstances[len(routes.classInstances) - 1]

class RouteHandle():

    def __init__(self):
        self._middleware = None
        self._prefix = None
        self._controller = None
        self._module = None
        self._verb = None
        self._method = None
        self._name = None
        self._uri = None

    def middleware(self, middleware:list = []):
        self._middleware = middleware
        return self

    def prefix(self,prefix:str):
        self._prefix = prefix
        return self

    def controller(self, classname:str):
        self._controller = classname
        return self

    def module(self, module:str):
        self._module = module
        return self

    def group(self, *args):

        # Eliminar el Registro Padre
        instances = _RouteInstances()
        instances.classInstances.remove(self)

        for instance in args:
            if not instance._middleware:
                instance._middleware = self._middleware
            if not instance._prefix:
                instance._prefix = self._middleware
            if not instance._controller:
                instance._controller = self._middleware
            if not instance._controller:
                instance._controller = self._middleware
            if not instance._module:
                instance._module = self._middleware
            if not instance._verb:
                instance._verb = self._middleware
            if not instance._method:
                instance._method = self._middleware
            if not instance._name:
                instance._name = self._middleware
            if not instance._uri:
                instance._uri = self._middleware

        return self

    def name(self, name:str):
        self._name = name
        return self

    def get(self, uri:str, method:str=None):
        self._uri = self._clean_uri(uri)
        self._verb = 'GET'
        self._method = method
        return self

    def post(self, uri:str, method:str=None):
        self._uri = self._clean_uri(uri)
        self._verb = 'POST'
        self._method = method
        return self

    def put(self, uri:str, method:str=None):
        self._uri = self._clean_uri(uri)
        self._verb = 'PUT'
        self._method = method
        return self

    def patch(self, uri:str, method:str=None):
        self._uri = self._clean_uri(uri)
        self._verb = 'PATCH'
        self._method = method
        return self

    def delete(self, uri:str, method:str=None):
        self._uri = self._clean_uri(uri)
        self._verb = 'DELETE'
        self._method = method
        return self

    def options(self, uri:str, method:str=None):
        self._uri = self._clean_uri(uri)
        self._verb = 'OPTIONS'
        self._method = method
        return self

    def action(self, action:str):
        self._method = action
        return self

    def _clean_uri(self, uri:str):
        """
        Cleans the given URI by standardizing its format. This includes replacing curly braces
        with angle brackets, removing extra slashes, and ensuring the URI starts and ends
        correctly.

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

        # Remove trailing slash if it exists (except for the root '/')
        if uri.endswith('/') and len(uri) > 1:
            uri = uri[:-1]

        return uri
