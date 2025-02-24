from typing import Any, Callable
from orionis.luminate.container.container import Container
from orionis.luminate.foundation.config.config_bootstrapper import ConfigBootstrapper
from orionis.luminate.foundation.console.command_bootstrapper import CommandsBootstrapper
from orionis.luminate.foundation.environment.environment_bootstrapper import EnvironmentBootstrapper
from orionis.luminate.patterns.singleton import SingletonMeta
from orionis.luminate.providers.commands.reactor_commands_service_provider import ReactorCommandsServiceProvider
from orionis.luminate.providers.commands.scheduler_provider import ScheduleServiceProvider
from orionis.luminate.providers.environment.environment__service_provider import EnvironmentServiceProvider
from orionis.luminate.providers.config.config_service_provider import ConfigServiceProvider
from orionis.luminate.providers.files.paths_provider import PathResolverProvider
from orionis.luminate.providers.log.log_service_provider import LogServiceProvider

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

    def __init__(self, container: Container):
        """
        Initializes the Application instance.

        Parameters
        ----------
        container : Container
            The dependency injection container for the application.
        """
        # Class attributes
        self._config: dict = {}
        self._commands: dict = {}
        self._environment_vars: dict = {}
        self._booted: bool = False

        # Initialize the application container
        self.container = container
        self.container.instance(container)
        self.boot()

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
        Bootstraps the application.

        This method is responsible for loading the environment, configuration, and core providers.
        It ensures the application is ready to handle requests or commands.
        """
        # Load environment server
        self._beforeBootstrapProviders()

        # Dynamically load application configuration
        self._bootstraping()

        # Load core providers
        self._afterBootstrapProviders()

        # Set the booted flag to True
        self._booted = True

    def _beforeBootstrapProviders(self):
        """
        Registers and boots essential providers required before bootstrapping.

        This method ensures that environment variables are loaded and available
        for use during the bootstrapping process.
        """
        # Load the path provider, which is responsible for resolving file paths.
        # Developers can interact with it through the facade "orionis.luminate.facades.files.paths.paths_facade.Paths".
        _path_provider = PathResolverProvider(app=self.container)
        _path_provider.register()
        _path_provider.boot()

        # Load the environment provider, which is responsible for returning values from the .env file.
        # This provider is essential as it must be loaded first to resolve environment variables.
        # Developers can interact with it through the facade "orionis.luminate.facades.environment.environment_facade.Env".
        _environment_provider = EnvironmentServiceProvider(app=self.container)
        _environment_provider.register()
        _environment_provider.boot()

    def _bootstraping(self):
        """
        Loads user-defined configuration, commands, and environment variables.

        This method initializes the configuration, commands, and environment variables
        required for the application to function.
        """
        # This initializer loads the user-defined configuration from the "config" folder.
        # It extracts configuration values and stores them as class properties for future use.
        config_bootstrapper_key = self.singleton(ConfigBootstrapper)
        config_bootstrapper: ConfigBootstrapper = self.make(config_bootstrapper_key)
        self._config = config_bootstrapper.get()

        # This initializer dynamically searches for all user-defined commands in the "commands" folder,
        # both from the framework core and developer-defined commands.
        # It stores them in a dictionary and registers them in the container.
        commands_bootstrapper_key = self.singleton(CommandsBootstrapper)
        commands_bootstrapper: CommandsBootstrapper = self.make(commands_bootstrapper_key)
        self._commands = commands_bootstrapper.get()
        for command in self._commands.keys():
            _key_instance_container = self.bind(self._commands[command].get('concrete'))
            self.alias(alias=command, concrete=_key_instance_container)

        # Load environment variables and store them as class properties.
        # This is useful for executing future tasks conditioned on environment values.
        environment_bootstrapper_key = self.singleton(EnvironmentBootstrapper)
        environment_bootstrapper: EnvironmentBootstrapper = self.make(environment_bootstrapper_key)
        self._environment_vars = environment_bootstrapper.get()

    def _afterBootstrapProviders(self):
        """
        Registers and boots additional providers after bootstrapping.

        This method ensures that configuration and logging providers are loaded
        and available for use in the application.
        """
        # Load the configuration provider, which is responsible for returning configuration values.
        # Developers can interact with it through the facade "orionis.luminate.facades.config.config_facade.Config".
        _environment_provider = ConfigServiceProvider(app=self.container)
        _environment_provider.register()
        _environment_provider.boot()

        # Load the log provider based on the application configuration defined by the developer.
        # Developers can interact with it through the facade "orionis.luminate.facades.log.log_facade.Log".
        _log_provider = LogServiceProvider(app=self.container)
        _log_provider.register()
        _log_provider.boot()

        # Load the scheduler provider, which is responsible for managing scheduled tasks.
        # Developers can interact with it through the facade "orionis.luminate.facades.scheduler.scheduler_facade.Schedule".
        _schedule_provider = ScheduleServiceProvider(app=self.container)
        _schedule_provider.register()
        _schedule_provider.boot()

        # Load the commands provider, which is responsible for executing and managing CLI commands.
        # Developers can interact with it through the facade "orionis.luminate.facades.commands.commands_facade.Commands".
        _commands_provider = ReactorCommandsServiceProvider(app=self.container)
        _commands_provider.register()
        _commands_provider.boot()