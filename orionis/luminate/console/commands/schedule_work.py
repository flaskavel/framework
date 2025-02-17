from orionis.luminate.console.register import register
from orionis.luminate.console.base.command import BaseCommand
from orionis.luminate.console.tasks.scheduler import Schedule
from orionis.luminate.contracts.console.task_manager_interface import ITaskManager

@register.command
class ScheduleWorkCommand(BaseCommand):
    """
    Command class to handle scheduled tasks within the Orionis application.

    This command initializes the scheduling system, registers the schedule,
    and starts the execution of scheduled tasks.
    """

    # The command signature used to execute this command.
    signature = "schedule:work"

    # A brief description of the command.
    description = "Starts the scheduled tasks."

    def handle(self) -> None:
        """
        Execute the scheduled tasks.

        This method initializes a Schedule instance, creates a TaskManager (Kernel),
        registers the schedule, and starts the execution of scheduled tasks.

        Raises
        ------
        RuntimeError
            If an unexpected error occurs during execution, a RuntimeError is raised
            with the original exception message.
        """
        try:

            # Initialize a new Schedule instance.
            schedule = Schedule()

            # Create an instance of the TaskManager to manage the scheduling.
            from app.console.tasks_manager import TaskManager  # type: ignore
            kernel: ITaskManager = TaskManager()
            kernel.schedule(schedule)

            # Start running the scheduled tasks using the schedule runner.
            schedule.start()

        except Exception as e:

            # Raise a RuntimeError if an unexpected error occurs.
            raise RuntimeError(f"An unexpected error occurred: {e}") from e
