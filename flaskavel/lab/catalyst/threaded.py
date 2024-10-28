import threading

class ConsoleThread:
    """
    ConsoleThread manages the creation and execution of a new thread,
    allowing configuration of daemon status and target function.
    """

    def __init__(self):
        """
        Initializes a ConsoleThread instance with default attributes.
        """
        self.isDaemon = False  # Indicates if the thread is a daemon
        self.target_function = None  # Stores the target function for the thread

    def daemon(self, isDaemon: bool = True) -> 'ConsoleThread':
        """
        Sets the daemon status for the thread.

        Args:
            isDaemon (bool): Whether the thread should run as a daemon.

        Returns:
            ConsoleThread: The current instance for method chaining.
        """
        self.isDaemon = isDaemon  # Set the daemon status
        return self  # Return the instance for chaining

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
        if not callable(function):  # Validate if the function is callable
            raise ValueError("The target must be a callable (function, method, etc.).")
        self.target_function = function  # Assign the target function
        return self  # Return the instance for chaining

    def start(self, *args, **kwargs) -> None:
        """
        Starts the thread with the target function and its arguments.

        Args:
            *args: Positional arguments for the target function.
            **kwargs: Keyword arguments for the target function.

        Raises:
            ValueError: If no target function has been set before starting.
        """
        # Ensure that the target function is set before starting the thread
        if self.target_function is None:
            raise ValueError("Target function must be set before starting the thread.")

        # Initialize the thread with the specified target function and daemon status
        job_thread = threading.Thread(target=self.target_function, args=args, kwargs=kwargs, daemon=self.isDaemon)
        job_thread.start()  # Start the thread
        job_thread.join()  # Wait for the thread to complete execution
