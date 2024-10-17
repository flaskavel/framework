import threading

class ConsoleThread:

    def __init__(self):
        self.isDaemon = False
        self.target_function = None

    def daemon(self, isDaemon: bool = True) -> 'ConsoleThread':
        """
        Sets the daemon status for the thread.

        Args:
            isDaemon (bool): Whether the thread should run as a daemon.

        Returns:
            ConsoleThread: The current instance for method chaining.
        """
        self.isDaemon = isDaemon
        return self

    def target(self, function: callable) -> 'ConsoleThread':
        """
        Sets the target function for the thread.

        Args:
            function (callable): The function to run in the thread.

        Returns:
            ConsoleThread: The current instance for method chaining.

        Raises:
            ValueError: If the target is not callable.
        """
        if not callable(function):
            raise ValueError("The target must be a callable (function, method, etc.).")
        self.target_function = function
        return self

    def start(self, *args, **kwargs) -> None:
        """
        Starts the thread with the target function and its arguments.

        Args:
            *args: Positional arguments for the target function.
            **kwargs: Keyword arguments for the target function.
        """

        if self.target_function is None:
            raise ValueError("Target function must be set before starting the thread.")

        job_thread = threading.Thread(target=self.target_function, args=args, kwargs=kwargs, daemon=self.isDaemon)
        job_thread.start()
        job_thread.join()