
from typing import Any
from datetime import datetime
from abc import ABC, abstractmethod

class IScheduleService(ABC):
    """
    A class that manages the scheduling of tasks using the APScheduler.

    Attributes
    ----------
    scheduler : BackgroundScheduler
        The background scheduler instance used to schedule tasks.
    callback : function | None
        A callback function that will be called when the scheduled task is triggered.

    Methods
    -------
    command(signature: str, vars: dict[str, Any] = {}, *args: Any, **kwargs: Any) -> 'Schedule':
        Defines a command to execute.
    """

    @abstractmethod
    def command(self, signature: str, vars: dict[str, Any] = {}, *args: Any, **kwargs: Any):
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

    @abstractmethod
    def onceAt(self, date: datetime):
        """
        Schedule the defined command to execute every X seconds.
        """
        pass

    @abstractmethod
    def everySeconds(self, seconds: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedule the defined command to execute every X seconds.
        """
        pass

    @abstractmethod
    def everySecond(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every second.
        """
        pass

    @abstractmethod
    def everyTwoSeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every two seconds.
        """
        pass

    @abstractmethod
    def everyFiveSeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every five seconds.
        """
        pass

    @abstractmethod
    def everyTenSeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every ten seconds.
        """
        pass

    @abstractmethod
    def everyFifteenSeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every fifteen seconds.
        """
        pass

    @abstractmethod
    def everyTwentySeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every twenty seconds.
        """
        pass

    @abstractmethod
    def everyThirtySeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every thirty seconds.
        """
        pass

    @abstractmethod
    def everyMinutes(self, minutes: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every X minutes.
        """
        pass

    @abstractmethod
    def everyMinute(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every minute.
        """
        pass

    @abstractmethod
    def everyTwoMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every two minutes.
        """
        pass

    @abstractmethod
    def everyThreeMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every three minutes.
        """
        pass

    @abstractmethod
    def everyFourMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every four minutes.
        """
        pass

    @abstractmethod
    def everyFiveMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every five minutes.
        """
        pass

    @abstractmethod
    def everyTenMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every ten minutes.
        """
        pass

    @abstractmethod
    def everyFifteenMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every fifteen minutes.
        """
        pass

    @abstractmethod
    def everyThirtyMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every thirty minutes.
        """
        pass

    @abstractmethod
    def hours(self, hours: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every X hours.
        """
        pass

    @abstractmethod
    def hourly(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every hour.
        """
        pass

    @abstractmethod
    def hourlyAt(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every hour at a specific minute.
        """
        pass

    @abstractmethod
    def everyOddHour(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every odd hour.
        """
        pass

    @abstractmethod
    def everyTwoHours(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every two hours.
        """
        pass

    @abstractmethod
    def everyThreeHours(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every three hours.
        """
        pass

    @abstractmethod
    def everyFourHours(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every four hours.
        """
        pass

    @abstractmethod
    def everySixHours(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every six hours.
        """
        pass

    @abstractmethod
    def days(self, days: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every X days.
        """
        pass

    @abstractmethod
    def daily(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute daily at midnight.
        """
        pass

    @abstractmethod
    def dailyAt(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute daily at a specific time.
        """
        pass

    @abstractmethod
    def twiceDaily(self, first_hour: int, second_hour: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute twice a day at specific hours.
        """
        pass

    @abstractmethod
    def monday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every Monday at a specific time.
        """
        pass

    @abstractmethod
    def tuesday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every tuesday at a specific time.
        """
        pass

    @abstractmethod
    def wednesday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every wednesday at a specific time.
        """
        pass

    @abstractmethod
    def thursday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every thursday at a specific time.
        """
        pass

    @abstractmethod
    def friday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every friday at a specific time.
        """
        pass

    @abstractmethod
    def saturday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every saturday at a specific time.
        """
        pass

    @abstractmethod
    def sunday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every sunday at a specific time.
        """
        pass

    @abstractmethod
    def weekly(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute weekly on Sunday at midnight.
        """
        pass

    @abstractmethod
    def start(self):
        """
        Starts the scheduler and stops automatically when there are no more jobs.
        """
        pass