from orionis.contracts.providers.i_service_provider import IServiceProvider
from orionis.luminate.container.container import Container
from orionis.luminate.services.files.path_service import PathService

class PathServiceProvider(IServiceProvider):

    def register(self, container: Container) -> None:
        """
        Registers services or bindings into the given container.

        Args:
            container (Container): The container to register services or bindings into.
        """
        self.key_sp = container.singleton(PathService)

    def boot(self, container: Container) -> None:
        """
        Boot the service provider.

        This method is intended to be overridden by subclasses to perform
        any necessary bootstrapping or initialization tasks.

        Args:
            container (Container): The service container instance.
        """
        container.make(self.key_sp)