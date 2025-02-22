from orionis.contracts.providers.i_service_provider import IServiceProvider
from orionis.luminate.container.container import Container
from orionis.luminate.services.config.config_service import ConfigService

class ConfigServiceProvider(IServiceProvider):

    def register(self, container: Container) -> None:
        """
        Registers services or bindings into the given container.

        Args:
            container (Container): The container to register services or bindings into.
        """
        self.key_sp = container.scoped(ConfigService)

    def boot(self, container: Container) -> None:
        """
        Boot the service provider.

        This method is intended to be overridden by subclasses to perform
        any necessary bootstrapping or initialization tasks.

        Args:
            container (Container): The service container instance.
        """
        container.make(self.key_sp)