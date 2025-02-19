from abc import ABC, abstractmethod
from typing import Any, Callable

class IContainer(ABC):
    """Service container and dependency injection."""

    @abstractmethod
    def bind(self, abstract: str, concrete: Callable[..., Any]) -> None:
        """Registers a service with a specific implementation.

        Args:
            abstract (str): Name or key of the service to register.
            concrete (Callable[..., Any]): Concrete implementation of the service.

        Raises:
            OrionisContainerException: If the service is already registered.
            TypeError: If the implementation is not a callable or instantiable class.
        """
        pass

    @abstractmethod
    def transient(self, abstract: str, concrete: Callable[..., Any]) -> None:
        """Registers a service as Transient, creating a new instance on each request.

        Args:
            abstract (str): Name or key of the service to register.
            concrete (Callable[..., Any]): Concrete implementation of the service.

        Raises:
            OrionisContainerException: If the service is already registered.
            TypeError: If the implementation is not a callable or instantiable class.
        """
        pass

    @abstractmethod
    def singleton(self, abstract: str, concrete: Callable[..., Any]) -> None:
        """Registers a service as Singleton, ensuring a single shared instance.

        Args:
            abstract (str): Name or key of the service to register.
            concrete (Callable[..., Any]): Concrete implementation of the service.

        Raises:
            OrionisContainerException: If the service is already registered.
            TypeError: If the implementation is not a callable or instantiable class.
        """
        pass

    @abstractmethod
    def scoped(self, abstract: str, concrete: Callable[..., Any]) -> None:
        """Registers a service as Scoped, shared within the same request.

        Args:
            abstract (str): Name or key of the service to register.
            concrete (Callable[..., Any]): Concrete implementation of the service.

        Raises:
            OrionisContainerException: If the service is already registered.
            TypeError: If the implementation is not a callable or instantiable class.
        """
        pass

    @abstractmethod
    def instance(self, abstract: str, instance: Any) -> None:
        """Registers a specific instance in the container, allowing it to be reused.

        Args:
            abstract (str): Name or key of the service to register.
            instance (Any): Specific instance of the service to register.

        Raises:
            OrionisContainerException: If the instance is already registered.
            ValueError: If the provided instance is of an unexpected or invalid type.
        """
        pass

    @abstractmethod
    def has(self, abstract: str) -> bool:
        """Checks if a service is registered in the container.

        Args:
            abstract (str): Name or key of the service to check.

        Returns:
            bool: True if the service is registered, False otherwise.

        Raises:
            ValueError: If the service name (abstract) is not a valid string.
        """
        pass

    @abstractmethod
    def alias(self, abstract: str, alias: str) -> None:
        """Creates an alias for a registered service, allowing access to the service using an alternative name.

        Args:
            abstract (str): Name or key of the original service.
            alias (str): The alias to assign to the service.

        Raises:
            OrionisContainerException: If the original service is not registered.
            ValueError: If the alias is not a valid string or is already in use.
        """
        pass

    @abstractmethod
    def make(self, abstract: str):
        """Automatically resolves a dependency, handling instances, singletons, scoped, transients, and aliases.

        This method resolves the dependencies of a service and handles the following service types:
        1. **Instances**: Returns a specific instance.
        2. **Singletons**: Returns the same unique instance each time.
        3. **Scoped**: Returns a shared instance within the same request.
        4. **Transients**: Creates a new instance each time.
        5. **Aliases**: Resolves an alias to the original service.

        Args:
            abstract (str): Name or key of the service to resolve.

        Returns:
            Any: The resolved instance or service.

        Raises:
            OrionisContainerException: If the service is not found.
        """
        pass

    @abstractmethod
    def call(self, instance: Any, method_name: str, **overrides):
        """Llama a un método del objeto resolviendo automáticamente las dependencias registradas.

        Args:
            instance (Any): Instancia del objeto en el cual se ejecutará el método.
            method_name (str): Nombre del método a llamar.
            **overrides: Argumentos que se deben pasar manualmente en lugar de resolverlos automáticamente.

        Returns:
            Any: El resultado de ejecutar el método con las dependencias resueltas.

        Raises:
            AttributeError: Si el método no existe en la instancia.
        """
        pass

    @abstractmethod
    def startRequest(self):
        """Starts a new request and clears the Scoped instances.

        This method should be called at the beginning of each request to ensure that
        scoped services do not persist between requests.
        """
        pass