from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.beaker.console.command import Command
from flaskavel.lab.beaker.scheduling.schedule import Schedule
from app.Console.Kernel import Kernel  # type: ignore

@reactor.register
class ScheduleWork(Command):
    """
    Command class to handle scheduled tasks within the Flaskavel application.
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

        # Print a new line for better readability in the console output
        self.newLine()

        # Inform the user that the scheduled jobs execution has started
        self.info(f"The execution of the scheduled jobs has started successfully.")
        self.newLine()

        # Initialize a new Schedule instance.
        schedule = Schedule()

        # Create an instance of the Kernel class to manage the scheduling.
        kernel = Kernel()

        # Schedule tasks in the kernel using the provided schedule instance.
        kernel.schedule(schedule=schedule)

        # Start running the scheduled tasks using the schedule runner.
        schedule.runner()
