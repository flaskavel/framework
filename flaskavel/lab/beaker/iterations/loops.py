import gc
import time
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.catalyst.threaded import ConsoleThread

class Loops:
    """
    A class to manage and execute scheduled loops with defined intervals.
    """

    def __init__(self):
        self.loops = []
        self.signature = None
        self.args = []
        self.sleep = 1
        self.timer = None
        self.isDaemon = False

    def daemon(self, isDaemon: bool = True):
        """
        Marks the threads as daemon, meaning they will exit when the main program exits.

        Returns:
            self: The current instance for method chaining.
        """
        self.isDaemon = isDaemon
        return self

    def command(self, signature: str, args: dict = {}):
        """
        Sets the command signature to be executed.

        Args:
            signature (str): The command signature.
            args (list): Optional list of arguments.

        Returns:
            self: The current instance for method chaining.
        """
        self.signature = signature.strip()
        self.args = []

        # Create Arguments.
        if len(args) > 0:
            for key, value in args.items():
                if ' ' in str(value):
                    self.args.append(f'--{key}="{value}"')
                else:
                    self.args.append(f'--{key}={value}')

        return self

    def intervals(self, sleep:int=1, timer:int|bool=None):
        """
        Defines the sleep and timer intervals for the loop.

        Args:
            sleep (int): The sleep duration between executions in seconds.
            timer (int): The total time before stopping the loop in seconds.

        Returns:
            self: The current instance for method chaining.

        Raises:
            ValueError: If the sleep or timer values are invalid.
        """
        if sleep < 1:
            raise ValueError("The sleep interval must be greater than or equal to 1 second to optimize CPU and memory usage.")

        if timer:
            if timer < 1:
                raise ValueError("The timer must be greater than or equal to 1 second.")
            if timer < sleep:
                raise ValueError("The timer must be greater than the sleep interval.")

        self.loops.append({
            'signature': self.signature,
            'args': self.args,
            'sleep': sleep,
            'timer': timer
        })

        return self

    def runner(self):
        """
        Initiates the execution of all registered loops.
        """
        for loop in self.loops:

            thread = ConsoleThread()
            thread.daemon(isDaemon=self.isDaemon)
            thread.target(function=self._run_job)
            thread.start(loop['signature'], loop['args'], loop['sleep'], loop['timer'])

    def _run_job(self, signature:str, args:dict, sleep:int, timer:int):
        """
        Executes a job with the specified signature and arguments, adhering to the defined sleep and timer intervals.

        Args:
            signature (str): The command signature to execute.
            args (list): The command arguments.
            sleep (int): The sleep duration between executions.
            timer (int): The total time before stopping the loop.
        """
        rerun = True
        elapsed_time = 0

        while rerun:
            try:
                # Execute command
                reactor.call(signature=signature, args=args)

                # Update the elapsed time
                elapsed_time += sleep

                # Stop if the timer has been reached
                if timer and elapsed_time >= timer:
                    rerun = False

                # Pause only if the job will rerun
                if rerun:
                    time.sleep(sleep)

                # Manually invoke garbage collection after each iteration
                gc.collect()

            except Exception as e:

                raise ValueError(f"Error occurred in Loop {self.signature}: {str(e)}")
