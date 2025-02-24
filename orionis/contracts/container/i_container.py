from abc import ABC, abstractmethod
from typing import Any, Callable

class IContainer(ABC):

    @abstractmethod
    def _ensureNotMain(self, concrete: Callable[..., Any]) -> str:
        """
        Ensure that a class is not defined in the main script.

        Parameters
        ----------
        concrete : Callable[..., Any]
            The class or function to check.

        Returns
        -------
        str
            The fully qualified name of the class.

        Raises
        ------
        OrionisContainerValueError
            If the class is defined in the main module.
        """
        pass

    @abstractmethod
    def _ensureUniqueService(self, obj: Any) -> None:
        """
        Ensure that a service is not already registered.

        Parameters
        ----------
        obj : Any
            The service to check.

        Raises
        ------
        OrionisContainerValueError
            If the service is already registered.
        """
        pass

    @abstractmethod
    def _ensureIsCallable(self, concrete: Callable[..., Any]) -> None:
        """
        Ensure that the given implementation is callable or instantiable.

        Parameters
        ----------
        concrete : Callable[..., Any]
            The implementation to check.

        Raises
        ------
        OrionisContainerTypeError
            If the implementation is not callable.
        """
        pass

    @abstractmethod
    def _ensureIsInstance(self, instance: Any) -> None:
        """
        Ensure that the given instance is a valid object.

        Parameters
        ----------
        instance : Any
            The instance to check.

        Raises
        ------
        OrionisContainerValueError
            If the instance is not a valid object.
        """
        pass

    @abstractmethod
    def forgetScopedInstances(self) -> None:
        """
        Reset scoped instances at the beginning of a new request.
        """
        self._scoped_instances = {}

    @abstractmethod
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
        pass

    @abstractmethod
    def transient(self, concrete: Callable[..., Any]) -> str:
        """
        Registers a transient service in the container.
        A transient service is created each time it is requested.
        Args:
            concrete (Callable[..., Any]): The callable that defines the service.
        Returns:
            str: The unique key generated for the callable.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def instance(self, instance: Any) -> str:
        """
        Registers an instance as a singleton in the container.
        Args:
            instance (Any): The instance to be registered as a singleton.
        Returns:
            str: The key under which the instance is registered in the container.
        """
        pass

    @abstractmethod
    def alias(self, alias: str, concrete: Any) -> None:
        """
        Creates an alias for a registered service.
        Args:
            alias (str): The alias name to be used for the service.
            concrete (Any): The actual service instance or callable to be aliased.
        Raises:
            OrionisContainerException: If the concrete instance is not a valid object or if the alias is a primitive type.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def _resolve(self, concrete: Callable[..., Any]) -> Any:
        """
        Resolve and instantiate a given service class or function.

        This method analyzes the constructor of the given class (or callable),
        retrieves its dependencies, and resolves them recursively, while respecting
        the service lifecycle.
        """
        pass

    @abstractmethod
    def _resolve_dependency(self, dep_type: Any) -> Any:
        """
        Resolves a dependency based on the provided type.

        This method looks for the type in the container and returns the instance,
        respecting the lifecycle of the service (transient, singleton, etc.).
        """
        pass