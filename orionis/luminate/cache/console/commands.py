from orionis.luminate.contracts.cache.cache_commands_interface import ICacheCommands

class CacheCommands(ICacheCommands):
    """
    Singleton class for managing a cache of commands.

    This class ensures that only one instance of the command cache exists
    and provides methods for registering, unregistering, and retrieving commands.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create or return the singleton instance of the CacheCommands class.

        Ensures that only one instance of the CacheCommands class exists
        during the lifetime of the application.

        Returns
        -------
        CacheCommands
            The singleton instance of the class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.commands = {}
        return cls._instance

    def register(self, signature: str, description: str, arguments: list, instance):
        """
        Register a new command with its signature, description, and class instance.

        Parameters
        ----------
        signature : str
            The unique identifier (signature) for the command.
        description : str
            A brief description of what the command does.
        instance : class
            The class or callable instance that defines the command behavior.

        Raises
        ------
        ValueError
            If a command with the given signature already exists.
        """
        if signature in self.commands:
            raise ValueError(f"Command '{signature}' is already registered. Please ensure signatures are unique.")

        self.commands[signature] = {
            'instance':instance,
            'arguments':arguments,
            'description':description,
            'signature':signature
        }

    def unregister(self, signature: str):
        """
        Unregister an existing command by its signature.

        Parameters
        ----------
        signature : str
            The unique identifier (signature) for the command to unregister.

        Raises
        ------
        KeyError
            If the command with the given signature does not exist.
        """
        if signature not in self.commands:
            raise KeyError(f"Command '{signature}' not found.")
        del self.commands[signature]

    def get(self, signature: str):
        """
        Retrieve the information of a registered command by its signature.

        Parameters
        ----------
        signature : str
            The unique identifier (signature) for the command.

        Returns
        -------
        dict
            A dictionary containing the class, signature, and description of the command.

        Raises
        ------
        KeyError
            If the command with the given signature does not exist.
        """
        command = self.commands.get(signature)
        if not command:
            raise KeyError(f"Command with signature '{signature}' not found.")
        return command
