import traceback
from orionis.luminate.container.container import Container
from orionis.luminate.bootstrap.config_bootstrapper import Bootstrapper as BootstrapperConfig
from orionis.luminate.patterns.singleton import SingletonMeta

class Application(metaclass=SingletonMeta):
    """
    The main service container for the Orionis Framework, ensuring persistent dependency resolution.

    This class acts as a singleton service container, similar to Laravel's Application class.
    It maintains service bindings, ensures proper initialization, and prevents unnecessary re-instantiation.

    Attributes
    ----------
    container : Container
        The IoC container that holds all service bindings.
    booted : bool
        Indicates whether the application has been initialized.
    error_info : tuple or None
        Stores error information if an exception occurs during boot.

    Methods
    -------
    boot()
        Initializes the application and registers all necessary dependencies.
    isBooted()
        Checks if the application is currently running.
    getError()
        Retrieves stored error information, if any.
    """

    def __init__(self):
        """Initializes the application with an empty dependency container."""
        self.container = Container()
        self.booted = False
        self.error_info = None

        self._config = {}

    def register(self):
        """
        Registers all necessary service bindings with the application container.

        This method is intended to be overridden by the user to define custom service bindings.
        """
        pass

    def boot(self):
        """
        Boots the application and registers necessary dependencies.

        This method ensures that all required services are bound to the container and instantiated.
        If the application is already booted, it returns immediately.

        Returns
        -------
        Application
            The current instance of the application.

        Raises
        ------
        Exception
            If an error occurs during the boot process.
        """
        if self.booted:
            return self

        try:
            # Config Bootstrapper and retrieve application configuration
            boot_config = self.container.singleton(BootstrapperConfig)
            app_config = self.container.make(boot_config)
            self._config = app_config.get()

            self.booted = True
            return self

        except Exception as e:
            # Capture and store exception details
            self.error_info = (e, traceback.format_exc())
            raise

    def isBooted(self):
        """
        Checks if the application has been successfully initialized.

        Returns
        -------
        bool
            True if the application has been booted, False otherwise.
        """
        return self.booted

    def getError(self):
        """
        Retrieves the last stored error details.

        Returns
        -------
        tuple or None
            A tuple containing the exception instance and its formatted traceback if an error occurred;
            otherwise, None.
        """
        return self.error_info