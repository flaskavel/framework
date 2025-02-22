import traceback
from orionis.luminate.container.container import Container
from orionis.luminate.cache.app.config import CacheConfig
from orionis.luminate.bootstrap.config.register import Register
from orionis.luminate.bootstrap.config.bootstrapper import Bootstrapper
from orionis.luminate.patterns.singleton import SingletonMeta

class Orionis(metaclass=SingletonMeta):
    """
    Manages the Orionis application lifecycle, ensuring proper initialization
    and cleanup while handling exceptions.
    """

    def __init__(self):
        """Initialize Orionis with a container and setup state tracking."""
        self.container = None
        self.is_started = False
        self.error_info = None

    def __enter__(self):
        """
        Starts the Orionis application and registers required dependencies.

        Returns
        -------
        Orionis
            The initialized Orionis instance.

        Raises
        ------
        Exception
            If an error occurs during startup.
        """
        try:
            if self.is_started:
                return self

            self.container = Container()

            self.container.singleton(CacheConfig)
            self.container.singleton(Register)
            self.container.singleton(Bootstrapper)

            self.container.make(Register)
            self.container.make(Bootstrapper)

            self.is_started = True
            return self

        except Exception as e:
            self.error_info = (e, traceback.format_exc())
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Cleans up resources and ensures proper shutdown.

        Returns
        -------
        bool
            False to propagate exceptions.
        """
        self.container = None
        self.is_started = False

        if exc_type:
            self.error_info = (exc_val, traceback.format_exc())
            return False

    def isStarted(self):
        """Check if Orionis is currently active."""
        return self.is_started

    def getError(self):
        """Retrieve stored error information."""
        return self.error_info


class OrionisContext:
    """
    Ensures that Orionis is running within a valid context before allowing access
    to the dependency container.
    """

    def __enter__(self):
        """
        Validates that Orionis is active and provides access to its container.

        Returns
        -------
        Container
            The Orionis container instance.

        Raises
        ------
        RuntimeError
            If Orionis is not running.
        """
        orionis = Orionis()
        if not orionis.isStarted():
            raise RuntimeError(
                "Error: Not running within a valid Orionis Framework context. "
                "Ensure that the Orionis application is correctly initialized."
            )
        return orionis

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures exceptions propagate naturally."""
        return False
