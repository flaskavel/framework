import time
from flaskavel.luminate.facades.log import Log
from flaskavel.luminate.console.output.console import Console
from flaskavel.luminate.console.output.executor import Executor
from flaskavel.luminate.pipelines.cli_pipeline import CLIPipeline
from flaskavel.luminate.contracts.console.runner_interface import ICLIRunner

class CLIRunner(ICLIRunner):
    """
    CLIRunner manages the execution of CLI commands in Flaskavel.

    This class:
    - Parses command-line arguments or function parameters.
    - Executes commands through the `CLIPipeline`.
    - Logs execution status and errors.

    Methods
    -------
    handle(signature: str = None, vars: dict = {}, *args, **kwargs)
        Processes and executes a CLI command based on provided arguments.
    """

    @staticmethod
    def handle(signature: str = None, vars: dict = {}, *args, **kwargs):
        """
        Processes and executes a CLI command.

        This method:
        - Determines whether the command is invoked from `sys.argv` or as a function.
        - Extracts the command signature and arguments.
        - Executes the command pipeline.
        - Logs execution status and handles errors.

        Parameters
        ----------
        signature : str, optional
            The command signature (default is None, meaning it is extracted from `sys.argv`).
        vars : dict, optional
            Named arguments for the command (default is an empty dictionary).
        *args
            Additional arguments for the command.
        **kwargs
            Additional keyword arguments for the command.

        Returns
        -------
        Any
            The output of the executed command.

        Raises
        ------
        ValueError
            If no command signature is provided.
        Exception
            If an unexpected error occurs during execution.
        """

        try:
            # Determine if command is being executed from sys.argv
            sys_argv = signature is None

            # Start execution timer
            start_time = time.perf_counter()

            # Handle command signature extraction from sys.argv
            if sys_argv:
                if not args or len(args[0]) <= 2:
                    raise ValueError("No command signature specified.")

                # Extract command signature and arguments
                args_list = args[0]
                signature, *args = args_list[2:]

            # Log command execution start
            Log.info(f"Running command: {signature}")
            Executor.running(program=signature)

            # Initialize command pipeline
            pipeline = CLIPipeline().getCommand(signature)

            # Parse arguments based on invocation type
            if sys_argv:
                pipeline.parseArguments(*args)
            else:
                pipeline.parseArguments(vars, *args, **kwargs)

            # Execute the command
            output = pipeline.execute()

            # Calculate execution time
            elapsed_time = round(time.perf_counter() - start_time, 2)

            # Log successful execution
            Log.success(f"Command executed successfully: {signature}")
            Executor.done(program=signature, time=f"{elapsed_time}s")

            return output

        except ValueError as e:

            # Handle missing or invalid command signature
            Console.error(message=f"Value Error: {e}")
            Log.error(f"Command failed: {signature or 'Unknown'}, Value Error: {e}")

            # Ensure execution time is recorded in failure cases
            elapsed_time = round(time.perf_counter() - start_time, 2)
            Executor.fail(program=signature or "Unknown", time=f"{elapsed_time}s")

        except Exception as e:

            # Handle unexpected errors
            Console.error(message=f"Execution Error: {e}")
            Log.error(f"Command failed: {signature or 'Unknown'}, Execution Error: {e}")

            # Ensure execution time is recorded in failure cases
            elapsed_time = round(time.perf_counter() - start_time, 2)
            Executor.fail(program=signature or "Unknown", time=f"{elapsed_time}s")
