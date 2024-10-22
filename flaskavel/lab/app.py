import os
import sys
import time
import json
import tempfile
from pathlib import WindowsPath
from flaskavel.lab.reagents.crypt import Crypt
from flaskavel.lab.catalyst.paths import _Paths
from flaskavel.lab.beaker.console.output import Console
from flaskavel.lab.catalyst.environment import _Environment

class Application:

    @staticmethod
    def configure(base_path:WindowsPath):
        try:
            return FlaskavelBootstrap(
                basePath=base_path
            )
        except Exception as e:
            Console.error(
                message=f"Critical Bootstrap Error in Flaskavel: {e}",
                timestamp=True
            )

class FlaskavelCache:

    def __init__(self, basePath: WindowsPath):
        self.basePath = basePath
        self.started_file = 'started.lab'

    def clearStart(self):
        started_file = os.path.join(tempfile.gettempdir(), self.started_file)
        if os.path.exists(started_file):
            os.remove(started_file)

    def validate(self):
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
        started_file = os.path.join(tempfile.gettempdir(), started_file)
        start_time = Crypt.encrypt(value=str(time.time()))
        with open(started_file, 'wb') as file:
            file.write(start_time.encode())


class FlaskavelBootstrap:

    def __init__(self, basePath):
        self.base_path = basePath
        self.cache = FlaskavelCache(basePath=self.base_path)

    def withRouting(self, api: list, web: list):
        self.apiRoutes = api
        self.webRoutes = web
        return self

    def withMiddlewares(self, aliases: dict, use: dict):
        self.aliasesMiddleware = aliases
        self.useMiddleware = use
        return self

    def create(self):
        if not self.cache.validate():
            self.cache.clearStart()

            _Environment(path=os.path.join(self.base_path, '.env'))
            _Paths(path=os.path.join(self.base_path))
            self._update_path()
            self._init()
            self.cache.register()

        return FlaskavelRunner(basePath=self.base_path)

    def _update_path(self):
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

    def _init(self):
        from config.cache import cache # type: ignore

        # Determina si se debe encriptar.
        encrypt = bool(cache['encrypt'])

        # Determina el almacenamiento del cache (por el momento file)
        store = cache['default']

        # Determina la ruta de guardado del cache de configuración
        path_cache_config = cache['store'][store]['config']
        path_routes_config = cache['store'][store]['routes']

        from config.app import app # type: ignore
        from config.auth import auth # type: ignore
        from config.cors import cors # type: ignore
        from config.database import database # type: ignore
        from config.filesystems import filesystems # type: ignore
        from config.logging import logging # type: ignore
        from config.mail import mail # type: ignore
        from config.queue import queue # type: ignore
        from config.session import session # type: ignore

        data_config = {
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

        json_data = json.dumps(data_config)

        config_cache = json_data
        if encrypt:
            config_cache = Crypt.encrypt(json_data)

        if os.path.exists(path_cache_config):
            os.remove(path_cache_config)

        with open(path_cache_config, 'wb') as file_cache_config:
            file_cache_config.write(config_cache.encode())

class FlaskavelRunner():

    def __init__(self, basePath):
        self._basePath =basePath

    def handleRequest(self, *args, **kwargs):
        return True

    def handleCommand(self, *args, **kwargs):
        from app.Console.Kernel import Kernel # type: ignore
        kernel = Kernel()
        kernel.set_start_time(time.time())
        kernel.set_base_path(str(self._basePath))
        kernel.handle(*args, **kwargs)