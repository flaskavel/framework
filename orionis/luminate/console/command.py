from typing import Any
from orionis.luminate.console.runner import CLIRunner
from orionis.luminate.contracts.console.command_interface import ICommand

class Command(ICommand):
    """
    Command class for managing and executing registered CLI commands.

    This class provides a static method to invoke commands registered in the
    `CacheCommands` singleton, passing the required signature and any additional
    parameters.

    Methods
    -------
    call(signature: str, vars: dict[str, Any] = {}, *args: Any, **kwargs: Any) -> Any
        Executes the specified command with the provided arguments.
    """

    @staticmethod
    def call(signature: str, vars: dict[str, Any] = {}, *args: Any, **kwargs: Any) -> Any:
        """
        Calls a registered command using the `CLIRunner`.

        Parameters
        ----------
        signature : str
            The command signature (name) to execute.
        vars : dict[str, Any], optional
            A dictionary containing named arguments for the command (default is `{}`).
        *args : Any
            Additional positional arguments.
        **kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        Any
            The output of the executed command.
        """
        return CLIRunner.handle(signature, vars, *args, **kwargs)
