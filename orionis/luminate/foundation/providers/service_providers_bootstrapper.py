import importlib
import inspect
import pathlib
from orionis.luminate.contracts.foundation.providers.i_service_providers_bootstrapper import IServiceProvidersBootstrapper
from orionis.luminate.container.container import Container
from orionis.luminate.foundation.exceptions.exception_bootstrapper import BootstrapRuntimeError
from orionis.luminate.providers.service_provider import ServiceProvider

class ServiceProvidersBootstrapper(IServiceProvidersBootstrapper):

    def __init__(self, container : Container) -> None:
        self._container = container
        self._before_providers = []
        self._after_providers = []
        self._autoload()

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

        base_path = pathlib.Path.cwd()

        command_dirs = [
            pathlib.Path(__file__).resolve().parent.parent.parent / "providers"
        ]

        for cmd_dir in command_dirs:
            if not cmd_dir.is_dir():
                continue

            for file_path in cmd_dir.rglob("*.py"):
                if file_path.name == "__init__.py":
                    continue

                module_path = ".".join(file_path.relative_to(base_path).with_suffix("").parts)

                # Remove 'site-packages.' prefix if present
                if 'site-packages.' in module_path:
                    module_path = module_path.split('site-packages.')[1]

                try:
                    module = importlib.import_module(module_path.strip())

                    # Find and register command classes
                    for name, concrete in inspect.getmembers(module, inspect.isclass):
                        if issubclass(concrete, ServiceProvider) and concrete is not ServiceProvider:
                            self._register(concrete)
                except Exception as e:
                    raise BootstrapRuntimeError(f"Error loading {module_path}") from e

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
        if concrete.beferoBootstrapping:
            self._before_providers.append(concrete)
        else:
            self._after_providers.append(concrete)

    def getBeforeServiceProviders(self) -> list:
        """
        Retrieve the registered service providers.

        Returns
        -------
        list
            A list of registered service providers
        """
        return self._before_providers

    def getAfterServiceProviders(self) -> list:
        """
        Retrieve the registered service providers.

        Returns
        -------
        list
            A list of registered service providers
        """
        return self._after_providers