import os
from threading import Lock
from flaskavel.luminate.console.command import Command
from flaskavel.luminate.tools.reflection import Reflection

class CLIKernel:
    """
    The Kernel class is a Singleton responsible for managing command loading and execution within the framework.
    It handles the initialization of command paths and the invocation of specified commands.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls):
        """Ensure only one instance of the Kernel class exists (Singleton pattern)."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CLIKernel, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the Kernel instance, loading commands if not already initialized."""
        if self._initialized:
            return

        self.paths = []
        self._load_commands()
        self._initialized = True

    def _load_commands(self):
        """
        Dynamically load command modules from the specified paths.

        This method walks through the command paths, locates Python files,
        and imports them as modules for use within the application. It ensures
        that only the main directories are iterated if they exist.
        """
        # Initialize the list of paths where commands are located
        paths = []

        # Define the base path
        base_path = os.getcwd()

        # Define the command directories
        command_dirs = [
            os.path.join(base_path, 'app', 'Console', 'Commands'),
            os.path.join(os.path.dirname(__file__), 'commands')
        ]

        # Add the valid directories to the paths list
        for command_dir in command_dirs:
            if os.path.isdir(command_dir):
                paths.append(command_dir)

        # Iterate through the valid paths
        for path in paths:
            # Walk through each valid path and find Python files to load as modules
            for current_directory, _, files in os.walk(path):
                # Only iterate through the main directories (i.e., no subdirectories)
                if current_directory == path:
                    pre_module = current_directory.replace(base_path, '').replace(os.sep, '.').lstrip('.')
                    for file in files:
                        if file.endswith('.py'):
                            # Construct the module name and path
                            module_name = file[:-3]  # Remove the '.py' extension
                            module_path = f"{pre_module}.{module_name}"

                            # Use Reflection to load the module
                            Reflection(module=module_path)