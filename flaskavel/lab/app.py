from pathlib import Path
from flaskavel.lab.synthesizer.bootstrap import FlaskavelBootstrap

class Application:
    """Application class to configure the Flaskavel framework."""

    @staticmethod
    def configure(base_path:Path):
        """Configure the Flaskavel framework with the given base path.

        Args:
            base_path (Path): The base path for the application.

        Returns:
            FlaskavelBootstrap: An instance of FlaskavelBootstrap configured with the base path.
        """
        return FlaskavelBootstrap(basePath=base_path)
