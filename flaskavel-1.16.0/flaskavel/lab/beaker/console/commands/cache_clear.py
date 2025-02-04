import os
import shutil
from flaskavel.lab.catalyst.config import Config
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.synthesizer.cache import FlaskavelCache

@reactor.register
class CacheClear(Command):
    """
    The CacheClear command is responsible for clearing the application's cached files,
    including configuration and routing caches as well as any Python bytecode caches (__pycache__).
    """

    # The command signature used to execute this command.
    signature = 'cache:clear'

    # A brief description of the command.
    description = 'Clears the project cache.'

    def handle(self) -> None:
        """
        Executes the command to clear the application cache by performing the following actions:
        1. Clears the base cache directory.
        2. Deletes specific cache files, including configuration and route caches.
        3. Recursively removes Python bytecode cache directories (__pycache__) within the base path.

        Returns:
            None
        """

        try:

            # Read bootstrap file.
            base_path = Config.bootstrap('base_path')
            config = Config.bootstrap('cache.config')
            routes = Config.bootstrap('cache.routes')

            # Initialize the cache clearing process
            FlaskavelCache(basePath=base_path).clearStart()

            # Remove configuration cache file if it exists
            if os.path.exists(config):
                os.remove(config)

            # Remove route cache file if it exists
            if os.path.exists(routes):
                os.remove(routes)

            # Recursively delete any __pycache__ directories found within the base path
            for root, dirs, files in os.walk(base_path):
                for dir in dirs:
                    if dir == '__pycache__':
                        pycache_path = os.path.join(root, dir)
                        shutil.rmtree(pycache_path)

            # Log a success message with a timestamp
            self.info(message='The application cache has been successfully cleared.', timestamp=True)

        except Exception as e:

            # Display general error message for any unexpected issue
            self.error(f"An unexpected error occurred: {e}" , timestamp=True)
            exit(1)