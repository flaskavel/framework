import os
from threading import Lock
from flaskavel.lab.catalyst.config import Config
from flaskavel.lab.catalyst.reflection import Reflection
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.register import native_commands

class Kernel:
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
                cls._instance = super(Kernel, cls).__new__(cls)
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

        This method walks through the command path, locates Python files,
        and imports them as modules for use within the application.
        """
        base_path = Config.bootstrap('base_path')
        commands_path = os.path.join(base_path, 'app', 'Console', 'Commands')

        # Load customer commands
        self._import_command_modules(commands_path, base_path)

        # Load native commands
        self._import_native_commands()

    def _import_command_modules(self, path: str, base_path: str):
        """
        Import Python files from the specified path as modules.

        Args:
            path (str): The path to search for command modules.
            base_path (str): The base path to normalize module paths.
        """
        for current_directory, _, files in os.walk(path):
            pre_module = current_directory.replace(base_path, '').replace(os.sep, '.').lstrip('.')
            for file in files:
                if file.endswith('.py'):
                    module_name = file[:-3]
                    module_path = f"{pre_module}.{module_name}"
                    Reflection(module=module_path)

    def _import_native_commands(self):
        """
        Import native command modules defined in the native_commands list.
        """
        for command in native_commands:
            Reflection(module=command['module'], classname=command['class'])

    def handle(self, *args):
        """
        Handle the execution of a command based on the provided arguments.

        This method retrieves the command name and its associated arguments,
        and invokes the specified command using the reactor.

        Args:
            *args: The command-line arguments passed to the application.
        """
        if len(args) == 0 or len(args[0]) < 2:
            raise ValueError("Invalid command arguments.")

        command = args[0][1]
        command_args = self._parse_command_args(args[0][2:])

        # Call the specified command using the reactor.
        reactor.call(command, command_args)

    def _parse_command_args(self, args):
        """
        Parse command arguments from the input list.

        Args:
            args (list): The list of command arguments.

        Returns:
            list: The parsed command arguments.
        """
        parsed_args = str('=').join(args).split('=')
        return [] if parsed_args == [''] else parsed_args
