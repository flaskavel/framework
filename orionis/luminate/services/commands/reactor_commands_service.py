import time
from typing import Any, Dict, Optional
from orionis.contracts.services.commands.i_reactor_commands_service import IReactorCommandsService
from orionis.luminate.bootstrap.command_bootstrapper import CommandsBootstrapper
from orionis.luminate.console.base.command import BaseCommand
from orionis.luminate.console.command_filter import CommandFilter
from orionis.luminate.console.exceptions.cli_exception import CLIOrionisException
from orionis.luminate.console.output.console import Console
from orionis.luminate.console.output.executor import Executor
from orionis.luminate.console.parser import Parser
from orionis.luminate.facades.app import app
from orionis.luminate.facades.log.log_facade import Log

class ReactorCommandsService(IReactorCommandsService):
    """
    Service responsible for executing and managing CLI commands in Orionis.

    This service handles:
    - Parsing command arguments.
    - Executing commands and logging their output.
    - Managing execution timing and error handling.
    """

    def __init__(
        self,
        commands_bootstrapper: CommandsBootstrapper,
        command_filter: CommandFilter,
        log: Log,
        executor: Executor,
        console: Console,
    ):
        """
        Initializes the ReactorCommandsService instance.

        Assigns provided services to internal attributes for later use in command
        execution, filtering, and logging.
        """
        self.commands_bootstrapper = commands_bootstrapper
        self.command_filter = command_filter
        self.log = log
        self.console_executor = executor
        self.console_output = console

    def _parse_arguments(
        self, arguments, vars: Optional[Dict[str, Any]] = None, *args, **kwargs
    ):
        """
        Parses command-line arguments using the Orionis argument parser.

        Utilizes an internal parser to convert raw arguments into structured data.
        Handles exceptions to ensure errors are properly raised and managed.
        """
        try:
            arg_parser = Parser(vars=vars or {}, args=args, kwargs=kwargs)
            arg_parser.setArguments(arguments=arguments)
            arg_parser.recognize()
            return arg_parser.get()
        except Exception as e:
            raise ValueError(f"Error parsing arguments: {e}")

    def _extract_arguments(self, args_dict:Any):
        """
        Extracts the arguments from the provided dictionary.

        Parameters
        ----------
        args_dict : Any
            A dictionary containing the arguments to extract.
        """
        try:
            return vars(args_dict)
        except Exception as e:
            raise ValueError(f"Error parsing arguments: {e}")

    def _call(self, signature: str, args_dict: Any) -> Any:
        """
        Executes the specified command with the provided arguments.

        Parameters
        ----------
        signature : str
            The command signature (name) to execute.
        args_dict : Any
            A dictionary containing named arguments for the command.
        """

        command_instance: BaseCommand = app(signature)
        command_instance.setArgs(args_dict)
        return command_instance.handle(**self._extract_arguments(args_dict))

    def execute(self, signature: Optional[str] = None, vars: dict = {}, *args, **kwargs):
        """
        Processes and executes a CLI command.

        Determines if the command originates from `sys.argv` or is explicitly called,
        then executes the appropriate command pipeline, handling success and errors.
        """
        try:

            # Determine if command is excluded from running
            exclude_running = self.command_filter.isExcluded(signature)
            sys_argv = signature is None

            # Start timing execution
            start_time = time.perf_counter()

            # Extract signature and arguments from command-line input
            if sys_argv:
                if not args or len(args[0]) <= 1:
                    raise CLIOrionisException("No command signature specified. Please provide a valid command to execute.")
                args_list = args[0]
                signature, *args = args_list[1:]

            # Log command execution
            self.log.info(f"Running command: {signature}")

            # Notify console
            if not exclude_running:
                self.console_executor.running(program=signature)

            # Retrieve command from bootstrapper
            command = self.commands_bootstrapper.get(signature)

            # Parse command arguments dynamically based on execution context
            args_dict = self._parse_arguments(command.get('arguments', []), vars, *args, **kwargs)

            # Exception handling for command execution
            output = self._call(signature, args_dict)

            # Log successful command execution
            self.log.success(f"Command executed successfully: {signature}")

            # Finalize execution and report elapsed time
            if not exclude_running:
                elapsed_time = round(time.perf_counter() - start_time, 2)
                self.console_executor.done(program=signature, time=f"{elapsed_time}s")

            # Return command output
            return output

        except ValueError as e:
            # Handle parsing errors
            self.log.error(f"Command failed: {signature or 'Unknown'}, Value Error: {e}")
            if not exclude_running:
                self.console_output.error(message=f"Value Error: {e}")
                elapsed_time = round(time.perf_counter() - start_time, 2)
                self.console_executor.fail(program=signature or "Unknown", time=f"{elapsed_time}s")
            self.console_output.exception(e)

        except Exception as e:
            # Handle unexpected execution errors
            self.log.error(f"Command failed: {signature or 'Unknown'}, Execution Error: {e}")
            if not exclude_running:
                self.console_output.error(message=f"Execution Error: {e}")
                elapsed_time = round(time.perf_counter() - start_time, 2)
                self.console_executor.fail(program=signature or "Unknown", time=f"{elapsed_time}s")
            self.console_output.exception(e)

