import os
from flaskavel.lab.beaker.console.output import Console

class App:
    """
    The App class is responsible for initializing and handling the application,
    including setting up the environment and executing the Kernel.
    """

    def __init__(self, base_path) -> None:
        """
        Initializes the App instance with the given base path.

        Args:
            base_path (str): The base path for the application.
        """
        self.base_path = os.path.dirname(base_path)

    def start(self, time):
        """
        Sets the start time for the application.

        Args:
            time (float): The time at which the application starts.

        Returns:
            App: The current instance of the App class.
        """
        self.time = time
        return self

    def make(self, module):
        """
        Stores the module information for later use.

        Args:
            module (str): The name of the module to be handled.

        Returns:
            App: The current instance of the App class.
        """
        self.module = module
        return self

    def handle(self, *args, **kwargs):
        """
        Handles the execution of the Kernel class.

        Args:
            *args: Positional arguments to pass to the Kernel.
            **kwargs: Keyword arguments to pass to the Kernel.
        """
        required_class_name = 'Kernel'

        # Dynamically import the Kernel class from the specified module
        module = __import__(self.module, fromlist=[required_class_name])
        class_kernel = getattr(module, required_class_name)

        try:
            # Instantiate the Kernel class and set up its properties
            kernel = class_kernel()
            kernel.set_start_time(self.time)
            kernel.set_base_path(self.base_path)

            # Call the handle method on the Kernel instance with provided arguments
            kernel.handle(*args, **kwargs)

        except Exception as e:

            # Handle any exceptions that occur during the execution
            Console.error(f"Flaskavel Runtime Error: {str(e)}")
