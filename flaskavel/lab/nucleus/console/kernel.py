import os
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.register import native_commands

class Kernel:
    """
    The Kernel class is responsible for managing command loading and execution within the framework.
    It handles the initialization of command paths and the invocation of specified commands.
    """

    def __init__(self) -> None:
        self.paths = []

    def set_start_time(self, start_time):
        """
        Store the start time of the application.

        Args:
            start_time (float): The time at which the application starts.
        """
        self.start_time = start_time

    def set_base_path(self, base_path):
        """
        Store the base path of the project.

        Args:
            base_path (str): The base directory path of the project.
        """
        self.base_path = base_path

    def load(self, directory, route):
        """
        Load command paths into the kernel.

        This method constructs the full path from the provided directory and route,
        and adds it to the list of paths if it is not already included.

        Args:
            directory (str): The base directory from which to construct the full path.
            route (str): The specific command route to append to the directory.
        """
        full_path = os.path.abspath(os.path.dirname(directory) + route)
        if full_path not in self.paths:
            self.paths.append(full_path)

    def load_commands(self, base_path):
        """
        Dynamically load command modules from the specified paths.

        This method walks through each path stored in `self.paths`, locates Python files,
        and imports them as modules for use within the application.

        Args:
            base_path (str): The base path to use for determining the module's location.
        """

        # Import Customer Commands
        for path in self.paths:
            for current_directory, subdirectory, files in os.walk(path):
                pre_module = str(current_directory).replace(base_path, '').replace(os.sep, '.').lstrip('.')
                for file in files:
                    if file.endswith('.py'):
                        module_name = file[:-3]  # Strip the .py extension
                        module_path = f"{pre_module}.{module_name}"
                        __import__(module_path)  # Import the module

        # Import Native Commands
        for command in native_commands:
            __import__(command['module'], fromlist=command['class'])


    def handle(self, *args):
        """
        Handle the execution of a command based on the provided arguments.

        This method retrieves the command name and its associated arguments from the input,
        loads the necessary command modules, and invokes the specified command.

        Args:
            *args: The command-line arguments passed to the application, where
                    the first element contains the command name and subsequent
                    elements are treated as command arguments.
        """
        # Retrieve the command to execute.
        command = args[0][1]
        args = str('=').join(args[0][2:]).split('=')

        # If the resulting list contains only an empty string, set args to an empty list
        if args == ['']:
            args = []

        # Load commands from the defined path.
        self.commands()

        # Load modules to call commands.
        self.load_commands(self.base_path)

        # Call the specified command using the reactor.
        reactor.start_time()
        reactor.call(command, args)