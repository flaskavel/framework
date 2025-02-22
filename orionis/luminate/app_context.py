from orionis.luminate.app import Application

class AppContext:
    """
    Context manager for resolving dependencies within a valid Orionis application context.

    This class ensures that Orionis is properly initialized before resolving dependencies,
    similar to how Laravel’s `app()` helper works.

    Methods
    -------
    __enter__()
        Validates the application state and provides access to the service container.
    __exit__(exc_type, exc_val, exc_tb)
        Ensures exceptions propagate naturally.
    """

    def __enter__(self):
        """
        Validates that the Orionis application is booted before allowing access to the container.

        Returns
        -------
        Container
            The application’s IoC container instance.

        Raises
        ------
        RuntimeError
            If the application has not been properly initialized.
        """
        app = Application()
        if not app.isBooted():
            raise RuntimeError(
                "Error: Not running within a valid Orionis Framework context. "
                "Ensure that the Orionis application is correctly initialized."
            )
        return app

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Allows exceptions to propagate naturally.

        Parameters
        ----------
        exc_type : type
            The exception type, if an error occurred.
        exc_val : Exception
            The exception instance, if an error occurred.
        exc_tb : traceback
            The traceback object associated with the exception, if an error occurred.

        Returns
        -------
        bool
            Always returns False to ensure exceptions are not suppressed.
        """
        return False