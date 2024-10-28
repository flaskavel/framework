from app.Console.Kernel import Kernel  # type: ignore
from flaskavel.lab.beaker.iterations.loops import Loops
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command

@reactor.register
class LoopsRun(Command):
    """
    This command is responsible for initiating the execution of loops configured in the Kernel.
    """

    # The command signature used to execute this command.
    signature = 'loops:run'

    # A brief description of the command.
    description = 'Start the execution of the loops loaded in the command Kernel.'

    def handle(self) -> None:
        """
        Executes the command by performing the following steps:
        1. Initializes the Loops instance for managing iterations.
        2. Instantiates the Kernel to load the specified loops.
        3. Starts the execution of the loops via the Loops runner method.

        Returns:
            None
        """

        # Initialize a new Loops instance to manage loop iterations
        loops = Loops()

        # Create an instance of the Kernel class to load and configure loops
        kernel = Kernel()

        # Load the loops into the Kernel
        kernel.loops(loop=loops)

        # Start the execution of the loaded loops
        loops.runner()
