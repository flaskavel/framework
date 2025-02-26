from typing import Any, Callable
from contextlib import contextmanager
from orionis.luminate.contracts.foundation.i_bootstraper import IBootstrapper
from orionis.luminate.container.container import Container
from orionis.luminate.foundation.config.config_bootstrapper import ConfigBootstrapper
from orionis.luminate.foundation.console.command_bootstrapper import CommandsBootstrapper
from orionis.luminate.foundation.environment.environment_bootstrapper import EnvironmentBootstrapper
from orionis.luminate.foundation.providers.service_providers_bootstrapper import ServiceProvidersBootstrapper
from orionis.luminate.patterns.singleton import SingletonMeta
from orionis.luminate.providers.service_provider import ServiceProvider

class Application(metaclass=SingletonMeta):
    """
    The core Application class responsible for bootstrapping and managing the application lifecycle.

    This class follows the Singleton pattern to ensure a single instance throughout the application.

    Attributes
    ----------
    _config : dict
        A dictionary to store application configuration.
    _commands : dict
        A dictionary to store application commands.
    _environment_vars : dict
        A dictionary to store environment variables.
    container : Container
        The dependency injection container for the application.

    Methods
    -------
    boot()
        Bootstraps the application by loading environment, configuration, and core providers.
    _beforeBootstrapProviders()
        Registers and boots essential providers required before bootstrapping.
    _bootstraping()
        Loads user-defined configuration, commands, and environment variables.
    _afterBootstrapProviders()
        Registers and boots additional providers after bootstrapping.
    """
    booted = False

    @classmethod
    def started(cls):
        """
        Marks the application as booted.
        """
        cls.booted = True

    @classmethod
    def getCurrentInstance(cls):
        """
        Returns the existing application instance if available.

        Returns
        -------
        Application
            The current singleton instance of the application.

        Raises
        ------
        RuntimeError
            If no instance has been initialized yet.
        """
        if cls not in SingletonMeta._instances:
            raise RuntimeError("Application has not been initialized yet. Please create an instance first.")
        return SingletonMeta._instances[cls]

    @classmethod
    def reset(cls):
        """
        Resets the application instance if it exists.

        This method is used to reset the application instance and clear the singleton instances
        stored in the `SingletonMeta` class.
        """
        if cls in SingletonMeta._instances:
            del SingletonMeta._instances[cls]

    def __init__(self, container: Container):
        """
        Initializes the Application instance.

        Parameters
        ----------
        container : Container
            The dependency injection container for the application.
        """
        # Class attributes
        self._before_boot_service_providers: list = []
        self._after_boot_service_providers: list = []
        self._config: dict = {}
        self._commands: dict = {}
        self._environment_vars: dict = {}
        self._booted: bool = False

        # Initialize the application container
        self.container = container
        self.container.instance(container)

    def isBooted(self) -> bool:
        """
        Check if the application has been booted.

        Returns
        -------
        bool
            True if the application has been booted, False otherwise.
        """
        return self._booted

    def bind(self, concrete: Callable[..., Any]) -> str:
        """
        Bind a callable to the container.
        This method ensures that the provided callable is not the main function,
        is unique within the container, and is indeed callable. It then creates
        a unique key for the callable based on its module and name, and stores
        the callable in the container's bindings.
        Args:
            concrete (Callable[..., Any]): The callable to be bound to the container.
        Returns:
            str: The unique key generated for the callable.
        """
        return self.container.bind(concrete)

    def transient(self, concrete: Callable[..., Any]) -> str:
        """
        Registers a transient service in the container.
        A transient service is created each time it is requested.
        Args:
            concrete (Callable[..., Any]): The callable that defines the service.
        Returns:
            str: The unique key generated for the callable.
        """
        return self.container.transient(concrete)

    def singleton(self, concrete: Callable[..., Any]) -> str:
        """
        Registers a callable as a singleton in the container.
        This method ensures that the provided callable is not the main module,
        is unique within the container, and is indeed callable. It then registers
        the callable as a singleton, storing it in the container's singleton registry.
        Args:
            concrete (Callable[..., Any]): The callable to be registered as a singleton.
        Returns:
            str: The key under which the singleton is registered in the container.
        """
        return self.container.singleton(concrete)

    def scoped(self, concrete: Callable[..., Any]) -> str:
        """
        Registers a callable as a scoped service.
        This method ensures that the provided callable is not the main service,
        is unique, and is indeed callable. It then registers the callable in the
        scoped services dictionary with relevant metadata.
        Args:
            concrete (Callable[..., Any]): The callable to be registered as a scoped service.
        Returns:
            str: The key under which the callable is registered in the scoped services dictionary.
        """
        return self.container.scoped(concrete)

    def instance(self, instance: Any) -> str:
        """
        Registers an instance as a singleton in the container.
        Args:
            instance (Any): The instance to be registered as a singleton.
        Returns:
            str: The key under which the instance is registered in the container.
        """
        return self.container.instance(instance)

    def alias(self, alias: str, concrete: Any) -> None:
        """
        Creates an alias for a registered service.
        Args:
            alias (str): The alias name to be used for the service.
            concrete (Any): The actual service instance or callable to be aliased.
        Raises:
            OrionisContainerException: If the concrete instance is not a valid object or if the alias is a primitive type.
        """
        return self.container.alias(alias, concrete)

    def has(self, obj: Any) -> bool:
        """
        Checks if a service is registered in the container.

        Parameters
        ----------
        obj : Any
            The service class, instance, or alias to check.

        Returns
        -------
        bool
            True if the service is registered, False otherwise.
        """
        return self.container.has(obj)

    def make(self, abstract: Any) -> Any:
        """
        Create and return an instance of a registered service.

        Parameters
        ----------
        abstract : Any
            The service class or alias to instantiate.

        Returns
        -------
        Any
            An instance of the requested service.

        Raises
        ------
        OrionisContainerException
            If the service is not found in the container.
        """
        return self.container.make(abstract)

    def forgetScopedInstances(self) -> None:
        """
        Reset scoped instances at the beginning of a new request.
        """
        return self.container.forgetScopedInstances()

    def boot(self):
        """
        Bootstraps the application by loading environment configuration and core providers.
        Notes
        -----
        The bootstrapping process involves several steps:
        1. Loading essential services.
        2. Executing pre-bootstrap provider hooks.
        3. Initializing core components.
        4. Executing post-bootstrap provider hooks.
        5. Loading command-line interface commands.
        After these steps, the application is marked as booted.
        """
        # Mark the application as booted
        Application.started()

        # Bootstrapping process
        self._bootServices()
        self._beforeBootstrapProviders()
        self._bootstrapping()
        self._afterBootstrapProviders()
        self._loadCommands()

    def _bootServices(self):
        """
        Bootstraps the application services.

        This method is responsible for loading the application's services. It reads all the
        ServiceProviders from the Core and those defined by the developer. Then, it stores
        in class dictionaries the services that need to be loaded before and after the Bootstrap.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        services_bootstrapper_key = self.singleton(ServiceProvidersBootstrapper)
        services_bootstrapper: ServiceProvidersBootstrapper = self.make(services_bootstrapper_key)
        self._before_boot_service_providers = services_bootstrapper.getBeforeServiceProviders()
        self._after_boot_service_providers = services_bootstrapper.getAfterServiceProviders()

    def _beforeBootstrapProviders(self):
        """
        Loads and registers essential services before bootstrapping.

        This method is responsible for loading and registering the services that are
        required before the main bootstrapping process. It iterates through the list
        of service providers that need to be initialized early, registers them, and
        then boots them to make sure they are ready for use.
        """
        for service in self._before_boot_service_providers:
            _environment_provider : ServiceProvider = service(app=self.container)
            _environment_provider.register()
            _environment_provider.boot()

    def _bootstrapping(self):
        """
        Loads configuration, commands, environment variables, and other bootstrappers.

        This method initializes and updates the class dictionaries with the results
        from various bootstrappers. It ensures that the application has the necessary
        configuration, commands, and environment variables loaded before proceeding
        with the rest of the bootstrapping process.
        """
        singletons_bootstrappers = [
            (self._config, ConfigBootstrapper),
            (self._commands, CommandsBootstrapper),
            (self._environment_vars, EnvironmentBootstrapper)
        ]
        for bootstrapper in singletons_bootstrappers:
            property_cls, bootstrapper_class = bootstrapper
            bootstrapper_key = self.singleton(bootstrapper_class)
            bootstrapper_instance : IBootstrapper = self.make(bootstrapper_key)
            property_cls.update(bootstrapper_instance.get())

    def _loadCommands(self):
        """
        Loads CLI commands, including both core system commands and those defined by the developer.

        This method iterates over the commands stored in the `_commands` attribute, binds each command 
        to its corresponding concrete implementation, and registers the command alias.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for command in self._commands.keys():
            data_command:dict = self._commands[command]
            id_container_concrete = self.bind(data_command.get('concrete'))
            self.alias(alias=command, concrete=id_container_concrete)

    def _afterBootstrapProviders(self):
        """
        Loads services into the container that depend on the Bootstrap process being completed.

        This method iterates over the list of service providers that need to be loaded after the
        Bootstrap process. For each service provider, it creates an instance, registers it, and
        then boots it.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        for service in self._after_boot_service_providers:
            _environment_provider : ServiceProvider = service(app=self.container)
            _environment_provider.register()
            _environment_provider.boot()

@contextmanager
def app_context():
    """
    Context manager for creating an instance of the Orionis application.

    This function initializes the Orionis application with a new container,
    ensuring that the application is properly set up before use.

    Yields
    ------
    Application
        The initialized Orionis application instance.

    Raises
    ------
    RuntimeError
        If the application has not been properly initialized.
    """
    try:

        # Check if the application has been booted
        if not Application.booted:
            app = Application(Container()).boot()
        else:
            app = Application.getCurrentInstance()

        # Yield the application instance
        yield app

    finally:

        # Close Context Manager
        pass

def app_booted():
    """
    Check if the application has been booted.

    Returns:
        bool: True if the application has been booted, False otherwise.
    """
    return Application.booted

def orionis():
    """
    Creates a new instance of the Orionis application.

    Ensures that any existing singleton instance of `Application` is removed before
    creating a fresh instance. It resets the singleton instances stored in `SingletonMeta`
    and `Container`.

    Returns
    -------
    Application
        A new instance of the Orionis application.
    """
    Container.reset()
    Application.reset()

    return Application(Container())
