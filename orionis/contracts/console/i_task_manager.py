from abc import ABC, abstractmethod
from orionis.luminate.console.tasks.scheduler import Schedule

class ITaskManager(ABC):
    """
    Abstract base class that defines the interface for managing tasks.

    This class provides an abstract method `schedule` that must be implemented by any
    subclass to define how tasks are scheduled.

    Methods
    -------
    schedule(schedule: Schedule) -> None
        Schedules a task based on the provided `Schedule` instance.
    """

    @abstractmethod
    def schedule(self, schedule: Schedule) -> None:
        """
        Schedules a task based on the given `Schedule` instance.

        This method is abstract and must be implemented by a subclass to define
        the specific scheduling logic.

        Parameters
        ----------
        schedule : Schedule
            An instance of the `Schedule` class, which contains the details of
            when and how the task should be executed.

        Returns
        -------
        None
            This method does not return anything, but it is expected to schedule
            the task as defined by the `schedule` object.
        """
        pass
