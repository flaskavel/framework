import os
from orionis.luminate.tools.reflection import Reflection

class CLICache:
    """
    Class responsible for managing the loading and execution of commands within the framework.

    This class ensures that commands are loaded only once and are accessible for execution.

    Attributes
    ----------
    paths : list
        List of directories where commands are located.

    Methods
    -------
    __init__ :
        Initializes the CLICache instance, loading commands if not already initialized.
    _load_commands :
        Loads command modules from predefined directories and imports them dynamically.
    """


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
        self.paths = []
        self._load_commands()

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

                            # Remove the '.py' extension
                            module_name = file[:-3]

                            # Construct the full module path
                            module_path = f"{pre_module}.{module_name}"

                            # Remove the 'site-packages' prefix from the module path
                            if 'site-packages.' in module_path:
                                module_path = module_path.split('site-packages.')[1]

                            # Use Reflection to load the module dynamically
                            Reflection(module=module_path)