from typing import Any
from orionis.contracts.facades.commands.i_commands_facade import ICommand
from orionis.luminate.facades.app import app
from orionis.luminate.services.commands.reactor_commands_service import ReactorCommandsService

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
        _commands_provider : ReactorCommandsService = app(ReactorCommandsService)
        return _commands_provider.execute(signature, vars, *args, **kwargs)
