import ast
import threading
from flaskavel.lab.reagents.crypt import Crypt

class _BootstrapCache:
    _instance = None  # Singleton instance
    _lock = threading.Lock()  # Lock for thread-safe instantiation

    def __new__(cls, path_cache_routes=None, path_cache_config=None, encrypt=False, key=None):
        """
        Creates or returns the singleton instance of _BootstrapCache.

        Args:
            path_cache_routes (str): Path to the cached routes file.
            path_cache_config (str): Path to the cached config file.
            encrypt (bool): Whether encryption is enabled for the cache.
            key (str): Key used for decrypting the cache if encryption is enabled.

        Returns:
            _BootstrapCache: Singleton instance of the _BootstrapCache class.
        """
        with cls._lock:  # Ensure thread-safe instantiation
            if cls._instance is None:
                cls._instance = super(_BootstrapCache, cls).__new__(cls)
                cls._instance._initialize(path_cache_routes, path_cache_config, encrypt, key)
        return cls._instance

    def _initialize(self, path_cache_routes, path_cache_config, encrypt, key):
        """
        Initializes the cache paths and loads data for routes and configuration.

        Args:
            path_cache_routes (str): Path to the cached routes file.
            path_cache_config (str): Path to the cached config file.
            encrypt (bool): Specifies if the cache files are encrypted.
            key (str): Encryption key to decrypt the cached files.

        Raises:
            ValueError: If the provided paths are invalid.
        """
        if not path_cache_routes or not path_cache_config:
            raise ValueError("Invalid cache paths provided. Please clear the cache to proceed.")

        # Load route and config data from cache files
        self.routes = self._load_cache(path_cache_routes, encrypt, key)
        self.config = self._load_cache(path_cache_config, encrypt, key)

    def _load_cache(self, path, encrypt, key):
        """
        Reads and optionally decrypts cache data from a given path.

        Args:
            path (str): Path to the cache file.
            encrypt (bool): Indicates if decryption is needed.
            key (str): Key to use for decryption if `encrypt` is True.

        Returns:
            dict: Parsed content of the cache file.
        """
        with open(path, 'r') as file:
            data = file.read()
            if encrypt == 'Y':  # Decrypt if encryption flag is set
                return ast.literal_eval(Crypt.decrypt(value=data, key=key))
            return ast.literal_eval(data)  # Directly parse if no encryption

    def get_routes(self):
        """
        Accesses the cached routes data.

        Returns:
            dict: Cached route data.
        """
        return self.routes

    def get_config(self):
        """
        Accesses the cached configuration data.

        Returns:
            dict: Cached configuration data.
        """
        return self.config
