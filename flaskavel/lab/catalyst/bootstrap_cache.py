import ast
import threading
from flaskavel.lab.reagents.crypt import Crypt

class _BootstrapCache:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, path_cache_routes=None, path_cache_config=None, encrypt=False, key=None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(_BootstrapCache, cls).__new__(cls)
                cls._instance._initialize(path_cache_routes, path_cache_config, encrypt, key)
        return cls._instance

    def _initialize(self, path_cache_routes, path_cache_config, encrypt, key):

        if not path_cache_routes or not path_cache_config:
            raise ValueError("Invalid cache paths provided. Please clear the cache to proceed.")

        self.routes = self._load_cache(path_cache_routes, encrypt, key)
        self.config = self._load_cache(path_cache_config, encrypt, key)

    def _load_cache(self, path, encrypt, key):
        with open(path, 'r') as file:
            data = file.read()
            if encrypt == 'Y':
                return ast.literal_eval(Crypt.decrypt(value=data, key=key))
            return ast.literal_eval(data)

    def get_routes(self):
        return self.routes

    def get_config(self):
        return self.config
