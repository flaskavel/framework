from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.beaker.scheduling.schedule import Schedule
from app.Console.Kernel import Kernel # type: ignore

@reactor.register
class ScheduleWork(Command):
    """
    Command class to handle scheduled tasks.
    """

    # The command signature used to execute this command.
    signature = 'schedule:work'

    # A brief description of the command.
    description = 'Starts the scheduled tasks'

    def handle(self) -> None:
        """
        Execute the scheduled tasks.

        This method initializes the Schedule and Kernel classes,
        registers the schedule, and starts the runner to execute
        the scheduled tasks.
        """

        self.newLine()
        self.info(f"The execution of the scheduled jobs has started successfully.")
        self.newLine()

        # Initialize a new Schedule instance.
        schedule = Schedule()

        # Create an instance of the Kernel class.
        kernel = Kernel()

        # Schedule tasks in the kernel.
        kernel.schedule(schedule=schedule)

        # Start running the scheduled tasks.
        schedule.runner()

