import os
from threading import Lock
from flaskavel.luminate.tools.reflection import Reflection
from flaskavel.luminate.cache.console.commands import CacheCommands
from flaskavel.luminate.contracts.console.cli_cache_interface import ICLICache

class CLICache(ICLICache):
    """
    Singleton class responsible for managing the loading and execution of commands within the framework.

    This class ensures that commands are loaded only once and are accessible for execution. It is designed to follow
    the Singleton pattern, meaning only one instance of this class will exist in the application lifecycle.

    Attributes
    ----------
    _instance : CLICache
        The singleton instance of the CLICache class.
    _lock : threading.Lock
        A lock used to ensure thread-safety during instance creation.
    _initialized : bool
        A flag indicating whether the class has been initialized.
    paths : list
        List of directories where commands are located.

    Methods
    -------
    __new__ :
        Creates and returns the singleton instance of the CLICache class.
    __init__ :
        Initializes the CLICache instance, loading commands if not already initialized.
    _load_commands :
        Loads command modules from predefined directories and imports them dynamically.
    getCommands :
        Returns the instance of CacheCommands containing the command cache.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls):
        """
        Ensures only one instance of the CLICache class exists (Singleton pattern).

        This method is responsible for controlling the instance creation process, ensuring that no more than one
        CLICache instance is created in the system, even in multi-threaded environments.

        Returns
        -------
        CLICache
            The singleton instance of the CLICache class.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CLICache, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the CLICache instance by loading commands if not already initialized.

        This method will load command modules only once, ensuring that the commands are available for execution
        across the application. It should not be called directly multiple times.

        Attributes
        ----------
        paths : list
            List of directories containing command files to be loaded.
        """
        if self._initialized:
            return

        self.paths = []
        self._load_commands()
        self._initialized = True

    def _load_commands(self):
        """
        Dynamically loads command modules from predefined directories.

        This method traverses the specified directories, locates Python files, and imports them as modules. 
        It ensures that only the main directories are iterated over, avoiding subdirectories.

        Directories searched:
        ---------------------
        - app/console/commands (relative to the base path)
        - Current directory of the module (this file's directory)
        """
        paths = []

        # Define the base path of the application
        base_path = os.getcwd()

        # Define command directories to be searched
        command_dirs = [
            os.path.join(base_path, 'app', 'console', 'commands'),
            os.path.join(os.path.dirname(__file__), 'commands')
        ]

        # Add valid directories to paths list
        for command_dir in command_dirs:
            if os.path.isdir(command_dir):
                paths.append(command_dir)

        # Iterate over each valid directory
        for path in paths:
            for current_directory, _, files in os.walk(path):
                # Ensure to only iterate through the top-level directories
                if current_directory == path:
                    pre_module = current_directory.replace(base_path, '').replace(os.sep, '.').lstrip('.')
                    for file in files:
                        if file.endswith('.py'):
                            # Construct the module name and path
                            module_name = file[:-3]  # Remove the '.py' extension
                            module_path = f"{pre_module}.{module_name}"

                            # Use Reflection to load the module dynamically
                            Reflection(module=module_path)

    def getCommands(self):
        """
        Returns the instance of the CacheCommands containing the command cache.

        This method provides access to the CacheCommands instance, which holds the loaded commands cache
        and makes it available for use.

        Returns
        -------
        CacheCommands
            The instance of CacheCommands that holds the cached commands.
        """
        return CacheCommands()
