from typing import Any, Tuple
from orionis.luminate.console.runner import CLIRunner
from orionis.luminate.contracts.console.kernel_interface import ICLIKernel

class CLIKernel(ICLIKernel):
    """
    CLIKernel acts as a bridge between the CLI entry point and the command runner.

    This class provides a static method to handle command execution via `CLIRunner`.

    Methods
    -------
    handle(*args: tuple[Any, ...]) -> Any
        Processes CLI arguments and delegates execution to `CLIRunner`.
    """

    @staticmethod
    def handle(*args: tuple[Any, ...]) -> Any:
        """
        Handles CLI command execution by forwarding arguments to `CLIRunner`.

        Parameters
        ----------
        *args : tuple[Any, ...]
            A tuple containing CLI arguments passed from the command line.

        Returns
        -------
        Any
            The result of the executed command.
        """
        return CLIRunner.handle(None, {}, *args)
