from abc import ABC, abstractmethod
from typing import Any
from orionis.luminate.services.commands.scheduler_service import ScheduleService

class ISchedule(ABC):

    @abstractmethod
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
        pass