from abc import ABC, abstractmethod

class IRegister(ABC):
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

    @abstractmethod
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
        pass