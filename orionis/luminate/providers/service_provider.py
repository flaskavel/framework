from orionis.contracts.providers.i_service_provider import IServiceProvider
from orionis.luminate.container.container import Container

class ServiceProvider(IServiceProvider):
    """
    Base class for service providers.

    Parameters
    ----------
    container : Container
        The container instance to be used by the service provider.
    """

    def __init__(self, app : Container) -> None:
        """
        Initialize the service provider with the given container.

        Parameters
        ----------
        container : Container
            The container instance to be used by the service provider.
        """
        self.app = app
        self.beferoBootstrapping = False

    def register(self) -> None:
        """
        Register services in the container.

        This method should be overridden in the subclass to register
        specific services.

        Parameters
        ----------
        container : Container
            The container instance where services will be registered.
        """
        raise NotImplementedError("This method should be overridden in the subclass")

    def boot(self) -> None:
        """
        Boot services in the container.

        This method should be overridden in the subclass to boot
        specific services.

        Parameters
        ----------
        container : Container
            The container instance where services will be booted.
        """
        raise NotImplementedError("This method should be overridden in the subclass")