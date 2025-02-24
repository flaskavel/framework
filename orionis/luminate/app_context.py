from contextlib import contextmanager
from orionis.luminate.app import Application
from orionis.luminate.container.container import Container

@contextmanager
def app_context():
    """
    Context manager for creating an instance of the Orionis application.

    This function initializes the Orionis application with a new container,
    ensuring that the application is properly set up before use.

    Yields
    ------
    Application
        The initialized Orionis application instance.

    Raises
    ------
    RuntimeError
        If the application has not been properly initialized.
    """
    try:

        # Check if the application has been booted
        if not Application.booted:
            # Create a new application instance
            app = Application(Container())
            app.boot()
        else:
            # Get the current application instance
            app = Application.getCurrentInstance()

        # Yield the application instance
        yield app

    finally:

        # Close Context Manager
        pass


def app_booted():
    """
    Context manager for creating an instance of the Orionis application.

    This function initializes the Orionis application with a new container,
    ensuring that the application is properly set up before use.

    Yields
    ------
    Application
        The initialized Orionis application instance.

    Raises
    ------
    RuntimeError
        If the application has not been properly initialized.
    """
    return Application.booted