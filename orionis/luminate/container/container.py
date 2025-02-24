import inspect
from collections import deque
from threading import Lock
from typing import Callable, Any, Dict, get_args, get_origin
from orionis.contracts.container.i_container import IContainer
from orionis.luminate.container.exception import OrionisContainerException, OrionisContainerValueError, OrionisContainerTypeError
from orionis.luminate.container.types import Types

BINDING = 'binding'
TRANSIENT = 'transient'
SINGLETON = 'singleton'
SCOPED = 'scoped'
INSTANCE = 'instance'

class Container(IContainer):
    """
    Service container and dependency injection manager.

    This class follows the singleton pattern to manage service bindings, instances,
    and different lifecycle types such as transient, singleton, and scoped.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._bindings = {}
                    cls._instance._transients = {}
                    cls._instance._singletons = {}
                    cls._instance._scoped_services = {}
                    cls._instance._instances = {}
                    cls._instance._aliases = {}
                    cls._instance._scoped_instances = {}
                    cls._instance._validate_types = Types()
        return cls._instance

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
        if concrete.__module__ == "__main__":
            raise OrionisContainerValueError("Cannot register a class from the main module in the container.")

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
        if self.has(obj):
            raise OrionisContainerValueError("The service is already registered in the container.")

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
        if not callable(concrete):
            raise OrionisContainerTypeError(f"The implementation '{str(concrete)}' must be callable or an instantiable class.")

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
        if not isinstance(instance, object) or instance.__class__.__module__ in ['builtins', 'abc']:
            raise OrionisContainerValueError(f"The instance '{str(instance)}' must be a valid object.")

    def forgetScopedInstances(self) -> None:
        """
        Reset scoped instances at the beginning of a new request.
        """
        self._scoped_instances = {}

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
        self._ensureNotMain(concrete)
        self._ensureUniqueService(concrete)
        self._ensureIsCallable(concrete)

        key = f"{concrete.__module__}.{concrete.__name__}"
        self._bindings[key] = {
            'concrete': concrete,
            'module': concrete.__module__,
            'name': concrete.__name__,
            'type': BINDING
        }

        return key

    def transient(self, concrete: Callable[..., Any]) -> str:
        """
        Registers a transient service in the container.
        A transient service is created each time it is requested.
        Args:
            concrete (Callable[..., Any]): The callable that defines the service.
        Returns:
            str: The unique key generated for the callable.
        """
        self._ensureNotMain(concrete)
        self._ensureUniqueService(concrete)
        self._ensureIsCallable(concrete)

        key = f"{concrete.__module__}.{concrete.__name__}"
        self._transients[key] = {
            'concrete': concrete,
            'module': concrete.__module__,
            'name': concrete.__name__,
            'type': TRANSIENT
        }

        return key

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
        self._ensureNotMain(concrete)
        self._ensureUniqueService(concrete)
        self._ensureIsCallable(concrete)

        key = f"{concrete.__module__}.{concrete.__name__}"
        self._singletons[key] = {
            'concrete': concrete,
            'module': concrete.__module__,
            'name': concrete.__name__,
            'type': SINGLETON
        }

        return key

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
        self._ensureNotMain(concrete)
        self._ensureUniqueService(concrete)
        self._ensureIsCallable(concrete)

        key = f"{concrete.__module__}.{concrete.__name__}"
        self._scoped_services[key] = {
            'concrete': concrete,
            'module': concrete.__module__,
            'name': concrete.__name__,
            'type': SCOPED
        }

        return key

    def instance(self, instance: Any) -> str:
        """
        Registers an instance as a singleton in the container.
        Args:
            instance (Any): The instance to be registered as a singleton.
        Returns:
            str: The key under which the instance is registered in the container.
        """
        self._ensureNotMain(instance.__class__)
        self._ensureUniqueService(instance)
        self._ensureIsInstance(instance)

        concrete = instance.__class__
        key = f"{concrete.__module__}.{concrete.__name__}"
        self._instances[key] = {
            'instance': instance,
            'module': concrete.__module__,
            'name': concrete.__name__,
            'type': INSTANCE
        }

        return key

    def alias(self, alias: str, concrete: Any) -> None:
        """
        Creates an alias for a registered service.
        Args:
            alias (str): The alias name to be used for the service.
            concrete (Any): The actual service instance or callable to be aliased.
        Raises:
            OrionisContainerException: If the concrete instance is not a valid object or if the alias is a primitive type.
        """

        if self._instance._validate_types.isPrimitive(alias):
            raise OrionisContainerException(f"Cannot use primitive type '{alias}' as an alias.")

        if isinstance(concrete, str):
            if self.has(concrete):
                current_key = concrete
            else:
                raise OrionisContainerException(f"Service '{concrete}' is not registered in the container.")
        elif isinstance(concrete, object) and concrete.__class__.__module__ not in ['builtins', 'abc']:
            cls_concrete = concrete.__class__
            current_key = f"{cls_concrete.__module__}.{cls_concrete.__name__}"
        elif callable(concrete):
            current_key = f"{concrete.__module__}.{concrete.__name__}"

        self._aliases[alias] = current_key

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
        if isinstance(obj, str):
            return obj in self._aliases or obj in (
                self._bindings | self._transients | self._singletons | self._scoped_services | self._instances
            )

        if isinstance(obj, object) and obj.__class__.__module__ not in {'builtins', 'abc'}:
            key = f"{obj.__class__.__module__}.{obj.__class__.__name__}"
            return key in self._instances

        if callable(obj):
            key = f"{obj.__module__}.{obj.__name__}"
            return key in (
                self._bindings | self._transients | self._singletons | self._scoped_services | self._aliases
            )

        return False

    def bound(self, abstract: Any) -> bool:
        """
        Checks if a service is bound in the container.

        Parameters
        ----------
        abstract : Any
            The service class or alias to check.

        Returns
        -------
        bool
            True if the service is bound, False otherwise.
        """
        return self.has(abstract)

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

        key = abstract

        if isinstance(abstract, str):
            key = self._aliases.get(key, key)

        if callable(abstract):
            key = f"{abstract.__module__}.{abstract.__name__}"

        if isinstance(abstract, object) and abstract.__class__.__module__ not in {'builtins', 'abc'}:
            key = f"{abstract.__class__.__module__}.{abstract.__class__.__name__}"

        if key in self._instances:
            return self._instances[key]['instance']

        if key in self._singletons:
            self._instances[key] = {'instance': self._resolve(self._singletons[key]['concrete'])}
            return self._instances[key]['instance']

        if key in self._scoped_services:
            if key not in self._scoped_instances:
                self._scoped_instances[key] = self._resolve(self._scoped_services[key]['concrete'])
            return self._scoped_instances[key]

        if key in self._transients:
            return self._resolve(self._transients[key]['concrete'])

        if key in self._bindings:
            return self._resolve(self._bindings[key]['concrete'])

        raise OrionisContainerException(f"Service '{abstract}' is not registered in the container.")

    def _resolve(self, concrete: Callable[..., Any]) -> Any:
        """
        Resolve and instantiate a given service class or function.

        This method analyzes the constructor of the given class (or callable),
        retrieves its dependencies, and resolves them recursively, while respecting
        the service lifecycle.
        """

        # Step 1: Retrieve the constructor signature of the class or callable.
        try:
            signature = inspect.signature(concrete)
        except ValueError as e:
            raise OrionisContainerException(f"Unable to inspect signature of {concrete}: {str(e)}")

        # Step 2: Prepare a dictionary for resolved dependencies and a queue for unresolved ones.
        resolved_dependencies: Dict[str, Any] = {}
        unresolved_dependencies = deque()

        # Step 3: Iterate through the parameters of the constructor.
        for param_name, param in signature.parameters.items():

            # Skip 'self' in methods
            if param_name == 'self':
                continue

            # Handle parameters that are VAR_POSITIONAL or VAR_KEYWORD
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            # If parameter has no annotation and no default value, it's unresolved
            if param.annotation is param.empty and param.default is param.empty:
                unresolved_dependencies.append(param_name)
                continue

            # Resolve parameters with default values (without annotations)
            if param.default is not param.empty:
                resolved_dependencies[param_name] = param.default
                continue

            # Resolve dependencies based on annotations (excluding primitive types)
            if param.annotation is not param.empty:
                param_type = param.annotation

                # Check if it's a generic type, get the origin type
                if get_origin(param_type) is not None:
                    param_type = get_args(param_type)[0]

                if isinstance(param_type, type) and not issubclass(param_type, (int, str, bool, float)):
                    if self.has(param_type):
                        resolved_dependencies[param_name] = self.make(f"{param_type.__module__}.{param_type.__name__}")
                    else:
                        resolved_dependencies[param_name] = self._resolve_dependency(param_type)
                else:
                    resolved_dependencies[param_name] = param_type

        # Step 4: Resolve any remaining unresolved dependencies.
        while unresolved_dependencies:
            dep_name = unresolved_dependencies.popleft()
            if dep_name not in resolved_dependencies:
                resolved_dependencies[dep_name] = self._resolve_dependency(dep_name)

        # Step 5: Instantiate the class with resolved dependencies.
        try:
            return concrete(**resolved_dependencies)
        except Exception as e:
            raise OrionisContainerException(f"Failed to instantiate {concrete}: {str(e)}")

    def _resolve_dependency(self, dep_type: Any) -> Any:
        """
        Resolves a dependency based on the provided type.

        This method looks for the type in the container and returns the instance,
        respecting the lifecycle of the service (transient, singleton, etc.).
        """
        # Check if the dependency exists in the container or create it if necessary, If it's a class type
        if isinstance(dep_type, type):
            if self.has(dep_type):
                # Resolves the service through the container
                return self.make(f"{dep_type.__module__}.{dep_type.__name__}")
            else:
                # Instantiate the class if not found in the container
                return self._resolve(dep_type)

        raise OrionisContainerException(f"Cannot resolve dependency of type {dep_type}")
