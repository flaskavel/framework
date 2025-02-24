from contextlib import contextmanager
from orionis.luminate.app import Application
from orionis.luminate.container.container import Container

@contextmanager
def app_context():
    """
    Context manager for resolving dependencies within a valid Orionis application context.

    This function ensures that Orionis is properly initialized before resolving dependencies,
    similar to how Laravel’s `app()` helper works.

    Yields
    ------
    Application
        The initialized Orionis application instance.

    Raises
    ------
    RuntimeError
        If the application has not been properly initialized.
    """
    container = Container()
    app = Application(container)

    if not app.isBooted():
        raise RuntimeError(
            "Error: Not running within a valid Orionis Framework context. "
            "Ensure that the Orionis application is correctly initialized."
        )

    try:
        yield app
    finally:
        pass
