import os
import time
import tempfile
from pathlib import Path
from flaskavel.lab.reagents.crypt import Crypt

class FlaskavelCache:
    """Handles caching mechanisms for the Flaskavel application."""

    def __init__(self, basePath:Path):
        """Initialize FlaskavelCache with the base path.

        Args:
            basePath (Path): The base path for the application.
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
