import traceback
from orionis.luminate.container.container import Container
from orionis.luminate.cache.app.config import CacheConfig
from orionis.luminate.bootstrap.config.register import Register
from orionis.luminate.bootstrap.config.bootstrapper import Bootstrapper
from orionis.luminate.patterns.singleton import SingletonMeta

class Orionis(metaclass=SingletonMeta):
    """
    Context manager for the Orionis application that handles startup and cleanup.

    This class manages the lifecycle of an Orionis application instance.
    It starts the application when entering the context and ensures that the
    application is properly finished when exiting, capturing any exceptions that occur.

    Attributes
    ----------
    is_started : bool
        Flag indicating whether the application has been successfully started.
    app : App
        Instance of the Orionis application.
    error_info : tuple or None
        Tuple containing the exception instance and its formatted traceback if an error occurs;
        otherwise, None.
    """

    def __init__(self):
        """
        Initialize the OrionisContext.

        Sets up the application instance and initializes state variables.
        """
        self.container = Container()
        self.is_started = False
        self.error_info = None

    def __enter__(self):
        """
        Enter the runtime context and start the application.

        Attempts to start the Orionis application. If successful, sets the active flag
        and returns the context instance. If an exception is raised during startup,
        captures the exception and its traceback before re-raising it.

        Returns
        -------
        OrionisContext
            The current context instance with the application started.

        Raises
        ------
        Exception
            Re-raises any exception that occurs during the application startup.
        """
        try:

            self.container.singleton(CacheConfig)
            self.container.singleton(Register)
            self.container.singleton(Bootstrapper)

            self.container.make(Register)
            self.container.make(Bootstrapper)

            self.is_started = True
            OrionisContext().is_started = True

            return self

        except Exception as e:

            self.error_info = (e, traceback.format_exc())
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and finish the application.

        Calls the application's finish method to perform cleanup regardless of whether
        an exception occurred. If an exception occurred, captures its information and
        returns False to indicate that the exception should not be suppressed.

        Parameters
        ----------
        exc_type : type
            The type of the exception raised (if any).
        exc_val : Exception
            The exception instance raised (if any).
        exc_tb : traceback
            The traceback associated with the exception (if any).

        Returns
        -------
        bool
            Always returns False so that any exception is propagated.
        """
        try:
            self.container = None
        finally:
            self.is_started = False

        if exc_type:
            self.error_info = (exc_val, traceback.format_exc())
            return False

    def isStarted(self):
        """
        Check if the application is currently active.

        Returns
        -------
        bool
            True if the application has been started and is active, False otherwise.
        """
        return self.is_started

    def getError(self):
        """
        Retrieve the stored error information.

        Returns
        -------
        tuple or None
            A tuple containing the exception and its formatted traceback if an error occurred;
            otherwise, None.
        """
        return self.error_info

class OrionisContext(metaclass=SingletonMeta):

    def __init__(self):
        self.is_started = False

    def __enter__(self):
        if self.is_started:
            return Orionis()
        raise Exception(
            "Error: Not running within a valid Orionis Framework context. "
            "Please ensure that you are using the proper context manager."
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass