from abc import ABC, abstractmethod
from orionis.luminate.container.container import Container

class IServiceProvider(ABC):

    @abstractmethod
    def register(self, container: Container) -> None:
        """
        Registers services or bindings into the given container.

        Args:
            container (Container): The container to register services or bindings into.
        """
        pass

    @abstractmethod
    def boot(self, container: Container) -> None:
        """
        Boot the service provider.

        This method is intended to be overridden by subclasses to perform
        any necessary bootstrapping or initialization tasks.

        Args:
            container (Container): The service container instance.
        """
        pass