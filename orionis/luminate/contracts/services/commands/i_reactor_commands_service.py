from abc import ABC, abstractmethod
from typing import Optional

class IReactorCommandsService(ABC):
    """
    Interface for the ReactorCommandsService class.
    Service responsible for executing and managing CLI commands in Orionis.

    This service handles:
    - Parsing command arguments.
    - Executing commands and logging their output.
    - Managing execution timing and error handling.
    """

    @abstractmethod
    def execute(self, signature: Optional[str] = None, vars: dict = {}, *args, **kwargs):
        """
        Processes and executes a CLI command.

        Determines if the command originates from `sys.argv` or is explicitly called,
        then executes the appropriate command pipeline, handling success and errors.
        """
        pass