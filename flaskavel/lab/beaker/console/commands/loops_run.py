from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.beaker.iterations.loops import Loops
from app.Console.Kernel import Kernel # type: ignore

@reactor.register
class LoopsRun(Command):
    """
    This command is responsible for initiating the execution of the loops.
    """

    # The command signature used to execute this command.
    signature = 'loops:run'

    # A brief description of the command.
    description = 'Start the execution of the loops loaded in the command Kernel.'

    def handle(self) -> None:
        """
        Unleashes the execution of the loops loaded in the kernel.
        """

        self.newLine()
        self.info(f"The execution of the scheduled loops has started successfully.")
        self.newLine()

        # Initialize a new Loops instance.
        loops = Loops()

        # Create an instance of the Kernel class.
        kernel = Kernel()

        # Load the loops.
        kernel.loops(loop=loops)

        # Start the execution.
        loops.runner()