from abc import ABC, abstractmethod
from orionis.luminate.providers.service_provider import ServiceProvider

class IServiceProvidersBootstrapper(ABC):

    @abstractmethod
    def _autoload(self) -> None:
        """
        Scans the provider directories and loads provider classes.

        This method searches for Python files in the specified directories, imports them,
        and registers any class that inherits from `ServiceProvider`.

        Raises
        ------
        BootstrapRuntimeError
            If there is an error loading a module.
        """
        pass

    @abstractmethod
    def _register(self, concrete: ServiceProvider) -> None:
        """
        Validates and registers a service provider class.

        This method ensures that the provided class is valid (inherits from `ServiceProvider`,
        has a `register` and `boot` method) and registers it in the
        `_service_providers` dictionary.

        Parameters
        ----------
        concrete : ServiceProvider
            The service provider class to register
        """
        pass

    @abstractmethod
    def getBeforeServiceProviders(self) -> list:
        """
        Retrieve the registered service providers.

        Returns
        -------
        list
            A list of registered service providers
        """
        pass

    @abstractmethod
    def getAfterServiceProviders(self) -> list:
        """
        Retrieve the registered service providers.

        Returns
        -------
        list
            A list of registered service providers
        """
        pass