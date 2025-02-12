from flaskavel.luminate.console.register import register
from flaskavel.luminate.console.base.command import BaseCommand
from flaskavel.luminate.console.tasks.scheduler import Schedule
from app.console.tasks_manager import TaskManager # type: ignore
from flaskavel.luminate.contracts.console.task_manager_interface import ITaskManager

@register.command
class ScheduleWork(BaseCommand):
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

        try:

            # Initialize a new Schedule instance.
            schedule = Schedule()

            # Create an instance of the Kernel class to manage the scheduling.
            kernel : ITaskManager = TaskManager()
            kernel.schedule(schedule)

            # Start running the scheduled tasks using the schedule runner.
            schedule.start()

        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")