from flaskavel.luminate.bootstrap.parser import Parser
from flaskavel.luminate.config.sections import SECTIONS
from flaskavel.luminate.tools.reflection import Reflection
from flaskavel.luminate.cache.app.config import CacheConfig
from flaskavel.luminate.contracts.config.config_interface import IConfig

class Register:
    """
    Handles the registration of configuration classes within the application.

    This class ensures that only valid configuration classes are registered
    while enforcing structure and type safety.

    Attributes
    ----------
    cache_config : CacheConfig
        An instance of `CacheConfig` used to store registered configurations.

    Methods
    -------
    config(config_class: type) -> type
        Registers a configuration class and ensures it meets the necessary criteria.
    """

    def __init__(self, cache: CacheConfig = None):
        """
        Initializes the Register instance with a cache configuration.

        Parameters
        ----------
        cache : CacheConfig, optional
            The cache configuration instance to be used (default is a new instance of `CacheConfig`).
        """
        self.cache_config = cache or CacheConfig()

    def config(self, config_class: type) -> type:
        """
        Registers a configuration class and ensures it meets the required structure.

        This method performs multiple validation steps, including checking if the input
        is a class, verifying the existence of a `config` attribute, and confirming
        inheritance from `IConfig`.

        Parameters
        ----------
        config_class : type
            The class to be registered as a configuration.

        Returns
        -------
        type
            The same class passed as an argument, if registration is successful.

        Raises
        ------
        TypeError
            If `config_class` is not a class or does not inherit from `IConfig`.
        ValueError
            If `config_class` does not have a `config` attribute or is already registered.
        """

        if not isinstance(config_class, type):
            raise TypeError(f"Expected a class, but got {type(config_class).__name__}.")

        if not hasattr(config_class, 'config'):
            raise ValueError(f"Class {config_class.__name__} must have a 'config' attribute.")

        # Extract module name
        section = Reflection(config_class).getFileName(remove_extension=True)

        # Validate section
        if section not in SECTIONS:
            raise ValueError(
                f"Invalid configuration section '{section}'. Allowed sections: {SECTIONS}"
            )

        # Validate inheritance
        if not issubclass(config_class, IConfig):
            raise TypeError(f"Class {config_class.__name__} must inherit from 'IConfig'.")

        # Check if section is already registered
        if section in self.cache_config.config:
            raise ValueError(f"Configuration section '{section}' is already registered.")

        # Register configuration
        self.cache_config.register(
            section=section,
            data=Parser.toDict(config_class)
        )

        # Return the original class
        return config_class

# Create a global Register instance
register = Register()
