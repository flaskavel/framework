import os
import shutil
from flaskavel.lab.catalyst.config import Config
from flaskavel.lab.synthesizer.cache import FlaskavelCache
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command

@reactor.register
class CacheClear(Command):

    # The command signature used to execute this command.
    signature = 'cache:clear'

    # A brief description of the command.
    description = 'Clears the project cache.'

    def handle(self) -> None:

        base_path = Config.bootstrap('base_path')
        config = Config.bootstrap('cache.config')
        routes = Config.bootstrap('cache.routes')

        FlaskavelCache(basePath=base_path).clearStart()

        if os.path.exists(config):
            os.remove(config)

        if os.path.exists(routes):
            os.remove(routes)

        for root, dirs, files in os.walk(base_path):
            for dir in dirs:
                if dir == '__pycache__':
                    pycache_path = os.path.join(root, dir)
                    shutil.rmtree(pycache_path)

        # Log the message with a timestamp
        self.info(message='The application cache has been successfully cleared', timestamp=True)
