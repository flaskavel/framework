from typing import Any
from orionis.contracts.facades.commands.i_scheduler_facade import ISchedule
from orionis.luminate.facades.app_facade import app
from orionis.luminate.services.commands.scheduler_service import ScheduleService

class Schedule(ISchedule):

    @staticmethod
    def command(signature: str, vars: dict[str, Any] = {}, *args: Any, **kwargs: Any) -> 'ScheduleService':
        """
        Defines a Orionis command to be executed.

        Parameters
        ----------
        signature : str
            The signature of the command to execute.
        vars : dict, optional
            A dictionary of variables to pass to the command, by default an empty dictionary.
        *args : Any
            Additional positional arguments to pass to the command.
        **kwargs : Any
            Additional keyword arguments to pass to the command.

        Returns
        -------
        Schedule
            Returns the Schedule instance itself, allowing method chaining.
        """
        _scheduler_provider : ScheduleService = app(ScheduleService)
        return _scheduler_provider.command(signature, vars, *args, **kwargs)

    @staticmethod
    def start():
        """
        Starts the scheduler and stops automatically when there are no more jobs.
        """
        _scheduler_provider : ScheduleService = app(ScheduleService)
        return _scheduler_provider.start()