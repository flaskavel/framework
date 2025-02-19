import inspect
from typing import Any, Callable
from orionis.luminate.container.exception import OrionisContainerException, OrionisContainerValueError

class Container:
    """Service container and dependency injection."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._bindings = {}
            cls._instance._transients = {}
            cls._instance._singletons = {}
            cls._instance._scoped_services = {}
            cls._instance._instances = {}
            cls._instance._aliases = {}
            cls._instance._scoped_instances = {}
            cls._instance._conditional_bindings = {}
        return cls._instance

    def bind(self, abstract: str, concrete: Callable[..., Any]) -> None:
        """Registers a service with a specific implementation.

        Args:
            abstract (str): Name or key of the service to register.
            concrete (Callable[..., Any]): Concrete implementation of the service.

        Raises:
            OrionisContainerException: If the service is already registered.
            TypeError: If the implementation is not a callable or instantiable class.
        """
        if self.has(abstract):
            raise OrionisContainerException(f"The service '{abstract}' is already registered in the container.")

        if not callable(concrete):
            raise TypeError(f"The implementation of '{abstract}' must be a callable or instantiable class.")

        self._bindings[abstract] = concrete

    def transient(self, abstract: str, concrete: Callable[..., Any]) -> None:
        """Registers a service as Transient, creating a new instance on each request.

        Args:
            abstract (str): Name or key of the service to register.
            concrete (Callable[..., Any]): Concrete implementation of the service.

        Raises:
            OrionisContainerException: If the service is already registered.
            TypeError: If the implementation is not a callable or instantiable class.
        """
        if self.has(abstract):
            raise OrionisContainerException(f"The service '{abstract}' is already registered in the container.")

        if not callable(concrete):
            raise TypeError(f"The implementation of '{abstract}' must be a callable or instantiable class.")

        self._transients[abstract] = concrete

    def singleton(self, abstract: str, concrete: Callable[..., Any]) -> None:
        """Registers a service as Singleton, ensuring a single shared instance.

        Args:
            abstract (str): Name or key of the service to register.
            concrete (Callable[..., Any]): Concrete implementation of the service.

        Raises:
            OrionisContainerException: If the service is already registered.
            TypeError: If the implementation is not a callable or instantiable class.
        """
        if self.has(abstract):
            raise OrionisContainerException(f"The service '{abstract}' is already registered in the container.")

        if not callable(concrete):
            raise TypeError(f"The implementation of '{abstract}' must be a callable or instantiable class.")

        self._singletons[abstract] = concrete

    def scoped(self, abstract: str, concrete: Callable[..., Any]) -> None:
        """Registers a service as Scoped, shared within the same request.

        Args:
            abstract (str): Name or key of the service to register.
            concrete (Callable[..., Any]): Concrete implementation of the service.

        Raises:
            OrionisContainerException: If the service is already registered.
            TypeError: If the implementation is not a callable or instantiable class.
        """
        if self.has(abstract):
            raise OrionisContainerException(f"The service '{abstract}' is already registered in the container.")

        if not callable(concrete):
            raise TypeError(f"The implementation of '{abstract}' must be a callable or instantiable class.")

        self._scoped_services[abstract] = concrete

    def instance(self, abstract: str, instance: Any) -> None:
        """Registers a specific instance in the container, allowing it to be reused.

        Args:
            abstract (str): Name or key of the service to register.
            instance (Any): Specific instance of the service to register.

        Raises:
            OrionisContainerException: If the instance is already registered.
            ValueError: If the provided instance is of an unexpected or invalid type.
        """
        if abstract in self._instances:
            raise OrionisContainerException(f"The instance '{abstract}' is already registered in the container.")

        if not isinstance(instance, object):
            raise ValueError(f"The instance of '{abstract}' must be a valid object.")

        self._instances[abstract] = instance

    def has(self, abstract: str) -> bool:
        """Checks if a service is registered in the container.

        Args:
            abstract (str): Name or key of the service to check.

        Returns:
            bool: True if the service is registered, False otherwise.

        Raises:
            ValueError: If the service name (abstract) is not a valid string.
        """
        # Check that 'abstract' is a string
        if not isinstance(abstract, str):
            raise ValueError(f"The service name '{abstract}' must be a string.")

        # Efficient check if the service is in any of the containers
        return any(abstract in container for container in [
            self._bindings,
            self._transients,
            self._singletons,
            self._scoped_services,
            self._instances
        ])

    def alias(self, abstract: str, alias: str) -> None:
        """Creates an alias for a registered service, allowing access to the service using an alternative name.

        Args:
            abstract (str): Name or key of the original service.
            alias (str): The alias to assign to the service.

        Raises:
            OrionisContainerException: If the original service is not registered.
            ValueError: If the alias is not a valid string or is already in use.
        """
        # Validate alias type
        if not isinstance(alias, str) or not alias:
            raise ValueError("The alias must be a non-empty string.")

        # Check if the original service is registered
        if not self.has(abstract):
            raise OrionisContainerException(f"The service '{abstract}' is not registered in the container.")

        # Check if the alias is already in use
        if alias in self._aliases:
            raise ValueError(f"The alias '{alias}' is already in use.")

        self._aliases[alias] = abstract

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
        # If the service is a specific instance, return it directly
        if abstract in self._instances:
            return self._instances[abstract]

        # If it is a singleton, return the same instance or resolve it if it is not yet resolved
        if abstract in self._singletons:
            if abstract not in self._instances:
                self._instances[abstract] = self._resolve(self._singletons[abstract])
            return self._instances[abstract]

        # If it is a scoped service, validate that it is in the same request context
        if abstract in self._scoped_services:
            if abstract not in self._scoped_instances:
                self._scoped_instances[abstract] = self._resolve(self._scoped_services[abstract])
            return self._scoped_instances[abstract]

        # If it is a transient service, create a new instance each time
        if abstract in self._transients:
            return self._resolve(self._transients[abstract])

        # If it is a regular binding, resolve it directly
        if abstract in self._bindings:
            return self._resolve(self._bindings[abstract])

        # If it is an alias, resolve the alias recursively
        if abstract in self._aliases:
            return self.make(self._aliases[abstract])

        raise OrionisContainerValueError(f"No definition found for '{abstract}'. Ensure the service is registered.")

    def _resolve(self, concrete: Callable[..., Any]):
        """Automatically resolves the dependencies of a service, handling its constructor dependencies.

        If the service is a class, it recursively resolves its dependencies (constructor parameters).

        Args:
            concrete (Callable[..., Any]): Concrete implementation of the service.

        Returns:
            Any: The resolved service instance.

        Raises:
            ValueError: If there is a constructor parameter whose type cannot be resolved.
        """
        if inspect.isclass(concrete):
            constructor = inspect.signature(concrete.__init__)
            parameters = constructor.parameters

            # If the class has no parameters in its constructor, instantiate it directly
            if len(parameters) == 0 or (len(parameters) == 1 and "self" in parameters):
                return concrete()

            # Resolve the dependencies of the class constructor
            dependencies = {}
            for name, param in parameters.items():
                if name == "self" or param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                    continue

                # If the parameter has a default value, use it directly
                param_type = param.annotation

                # If the parameter type is not specified, try to resolve it by name
                if param_type == param.empty:
                    if param.default != param.empty:
                        # Use the default value if available
                        continue

                    raise OrionisContainerValueError(f"Parameter type {name} not specified in {concrete.__name__}")

                # If the parameter type is a primitive, use it directly
                dep_name = param_type.__name__

                # Conditional resolution of dependencies, if registered
                if concrete in self._conditional_bindings and dep_name in self._conditional_bindings[concrete]:
                    dependencies[name] = self.make(self._conditional_bindings[concrete][dep_name])
                else:
                    dependencies[name] = self.make(dep_name)

            return concrete(**dependencies)

        return concrete(self)

    def startRequest(self):
        """Starts a new request and clears the Scoped instances.

        This method should be called at the beginning of each request to ensure that
        scoped services do not persist between requests.
        """
        self._scoped_instances = {}