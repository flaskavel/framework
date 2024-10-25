import os
import json
import time
import tempfile
from pathlib import Path
from flaskavel.lab.reagents.crypt import Crypt
from flaskavel.lab.catalyst.bootstrap_cache import _BootstrapCache

class FlaskavelCache:
    """Handles caching mechanisms for the Flaskavel application."""

    def __init__(self, basePath:Path):
        """Initialize FlaskavelCache with the base path.

        Args:
            basePath (Path): The base path for the application.
        """
        self.basePath = basePath
        self.root_project = str(os.path.dirname(__file__)).replace(os.sep, '_').lower()
        self.started_file = self.root_project + 'started.lab'

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
        started_file_path = os.path.join(tempfile.gettempdir(), self.started_file)

        # Check if the started file exists
        if not os.path.isfile(started_file_path):
            return False

        # Read and decrypt start time
        with open(started_file_path, 'r') as file:
            text = Crypt.decrypt(value=file.read())

        data_list = json.loads(text)
        self.time = float(data_list['time'])
        self.path_cache_config = data_list['path_cache_config']
        self.path_cache_routes = data_list['path_cache_routes']
        self.encrypt = data_list['encrypt']
        self.key = data_list['key']

        # Get last modification time of the .env file
        env_path = os.path.join(self.basePath, '.env')
        if os.path.getmtime(env_path) >= self.time:
            return False

        # Get last modification time of app.py
        app_path = os.path.join(self.basePath, 'bootstrap', 'app.py')
        if os.path.getmtime(app_path) >= self.time:
            return False

        # Check last modification times of all files in the config directory
        config_path = os.path.join(self.basePath, 'config')
        for file_name in os.listdir(config_path):
            full_path = os.path.join(config_path, file_name)
            if os.path.isfile(full_path) and os.path.getmtime(full_path) >= self.time:
                return False

        return True

    def register(self, path_cache_config, path_cache_routes, encrypt, key, started_file: str = 'started.lab'):
        """Register the start time in the cache.

        Args:
            started_file (str): The name of the started file to create.
        """
        self.time = str(time.time())
        self.path_cache_config = path_cache_config
        self.path_cache_routes = path_cache_routes
        self.encrypt = 'Y' if encrypt else 'N'
        self.key = key

        text_init = {
            'time': self.time,
            'path_cache_config': self.path_cache_config,
            'path_cache_routes': self.path_cache_routes,
            'encrypt': self.encrypt,
            'key': self.key
        }

        started_file = os.path.join(tempfile.gettempdir(), started_file)
        text = Crypt.encrypt(value=json.dumps(text_init))
        with open(started_file, 'wb') as file:
            file.write(text.encode())

    def mount(self):
        """Mount cache from files"""
        _BootstrapCache(
            path_cache_routes=self.path_cache_routes,
            path_cache_config=self.path_cache_config,
            encrypt=self.encrypt,
            key=self.key
        )
