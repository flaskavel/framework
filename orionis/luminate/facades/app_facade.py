from typing import Any
from orionis.luminate.application import app_booted
from orionis.luminate.console.output.console import Console
from orionis.luminate.container.container import Container

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

        # Error message
        message = "The application context is invalid. Use <with app_context() as cxt:> or ensure that the application is running."

        # Print error in console
        Console.textMuted("-" * 50)
        Console.error(message)
        Console.textMuted("-" * 50)

        # Raise exception
        raise RuntimeError(message)

    # Call the container instance
    container = Container()

    # If concrete is provided (not None), attempt to resolve it from the container
    if concrete is not None:
        return container.make(concrete)

    # If concrete is None, return the container instance
    return container
