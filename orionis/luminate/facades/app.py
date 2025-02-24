from typing import Any
from orionis.luminate.application import app_booted
from orionis.luminate.console.output.console import Console
from orionis.luminate.container.container import Container
from orionis.luminate.container.exception import OrionisContainerException, OrionisContainerTypeError

def app(concrete: Any = None):
    """
    Retrieves the container instance or resolves a service from the container.

    If a `concrete` class or service is passed, it will check if it is bound
    to the container and return an instance of the service. If not bound,
    an exception will be raised.

    Parameters
    ----------
    concrete : Any, optional
        The concrete service or class to resolve from the container.
        If None, returns the container instance itself.

    Returns
    -------
    Container or Any
        If `concrete` is provided and bound, returns the resolved service.
        If `concrete` is None, returns the container instance.

    Raises
    ------
    OrionisContainerException
        If `concrete` is not bound to the container.
    """
    if not app_booted():
        Console.error("The application context is not valid.")
        raise OrionisContainerException("The application context is not valid.")

    # Create a new container instance
    container : Container = Container()

    # If concrete is provided (not None), attempt to resolve it from the container
    if concrete is not None:
        return container.make(concrete)

    # If concrete is None, return the container instance
    return container
