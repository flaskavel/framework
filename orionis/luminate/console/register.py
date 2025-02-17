from orionis.luminate.console.base.command import BaseCommand
from orionis.luminate.cache.console.commands import CacheCommands
from orionis.luminate.contracts.console.register_interface import IRegister

class Register(IRegister):
    """
    A class to register and manage command classes.

    Attributes
    ----------
    commands : dict
        A dictionary storing registered command classes.
    """

    def __init__(self, cache : CacheCommands = None):
        """
        Initializes the Register instance and prepares the cache commands system.
        """
        self.cache_commands = cache or CacheCommands()

    def command(self, command_class):
        """
        Registers a command class after validating its structure.

        Parameters
        ----------
        command_class : type
            The command class to register. It must:
            - Have a 'signature' attribute (str, containing only letters, numbers, and ':', with no spaces).
            - Have a 'description' attribute (str).
            - Implement a 'handle' method.
            - Inherit from 'BaseCommand'.

        Returns
        -------
        type
            The registered command class.

        Raises
        ------
        ValueError
            If 'signature' is missing, invalid, contains spaces, or is not a string.
            If 'description' is missing or not a string.
            If 'handle' method is missing.
        TypeError
            If the class does not inherit from 'BaseCommand'.
        """

        # Ensure 'command_class' is actually a class
        if not isinstance(command_class, type):
            raise TypeError(f"Expected a class, but got {type(command_class).__name__}.")

        # Validate 'signature' attribute
        if not hasattr(command_class, 'signature') or not isinstance(command_class.signature, str):
            raise ValueError(f"Class {command_class.__name__} must have a 'signature' attribute as a string.")

        # Sanitaze signature
        signature = command_class.signature.strip()

        # Ensure signature contains only letters, numbers, and ':', with no spaces
        if not signature or ' ' in signature or not all(c.isalnum() or c == ":" for c in signature):
            raise ValueError(f"Invalid signature format: '{signature}'. Only letters, numbers, and ':' are allowed, with no spaces.")

        # Validate 'description' attribute
        if not hasattr(command_class, 'description') or not isinstance(command_class.description, str):
            raise ValueError(f"Class {command_class.__name__} must have a 'description' attribute as a string.")

        # Sanitaze signature
        description = command_class.description.strip()

        # Validate 'handle' method
        if not hasattr(command_class, 'handle') or not callable(getattr(command_class, 'handle')):
            raise ValueError(f"Class {command_class.__name__} must implement a 'handle' method.")

        # Validate 'arguments' method
        if hasattr(command_class, 'arguments') and callable(getattr(command_class, 'arguments')):
            arguments = command_class().arguments()
        else:
            arguments = []

        # Validate inheritance from 'BaseCommand'
        if not issubclass(command_class, BaseCommand):
            raise TypeError(f"Class {command_class.__name__} must inherit from 'BaseCommand'.")

        # Register the command
        self.cache_commands.register(
            instance=command_class,
            arguments=arguments,
            description=description,
            signature=signature
        )

        # Return Class
        return command_class


# Return Decorator.
register = Register()
