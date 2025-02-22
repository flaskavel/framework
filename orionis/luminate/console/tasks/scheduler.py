import logging
import re
import sys
import time
from datetime import datetime
from typing import Any
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from orionis.contracts.console.tasks.i_schedule import ISchedule
from orionis.luminate.app_context import AppContext
from orionis.luminate.console.command import Command
from orionis.luminate.console.exceptions.cli_exception import CLIOrionisScheduleException

class Schedule(ISchedule):
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

    def __init__(self, logger_level=logging.CRITICAL):
        """
        Initializes the Schedule object.

        This method sets up the background scheduler, starts it, and configures the logging level for APScheduler.

        Parameters
        ----------
        logger_level : int, optional
            The logging level for the APScheduler logger. Default is `logging.CRITICAL` to suppress most logs.
        """
        logging.getLogger("apscheduler").setLevel(logger_level)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.callback = None
        self.wait = True

    def command(self, signature: str, vars: dict[str, Any] = {}, *args: Any, **kwargs: Any) -> 'Schedule':
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
        def func():
            try:
                with AppContext() as app:
                    app.container.makeCommand(signature, vars, *args, **kwargs)
            finally:
                if not self.scheduler.get_jobs():
                    self.wait = False

        self.callback = func
        return self

    def _checkCommand(self):
        """
        Raises an exception to test the exception handling in the CLI.
        """
        if not self.callback:
            raise CLIOrionisScheduleException("No command has been defined to execute.")

    def _resetCallback(self):
        """
        Resets the callback function to None.
        """
        self.callback = None

    def _hourFormat(self, at: str):
        """
        Validates the time format in 'HH:MM' 24-hour format.
        """
        if not isinstance(at, str):
            raise CLIOrionisScheduleException("Time must be a string in 'HH:MM' format. Example: '23:59'.")

        # Regular expression for the "HH:MM" 24-hour format
        pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"

        if not re.match(pattern, at):
            raise CLIOrionisScheduleException("Invalid time format. Expected 'HH:MM' (24-hour format). Example: '23:59'.")

        return at.split(':')

    def _checkDateTime(self, start_date: datetime = None, end_date: datetime = None):
        """
        Validates the `start_date` and `end_date` parameters.

        Ensures that both parameters are either `None` or valid `datetime` instances.
        Additionally, it verifies that `start_date` is earlier than `end_date` if both are provided.

        Parameters
        ----------
        start_date : datetime, optional
            The start time of the scheduled job. Must be a valid `datetime` object if provided.
        end_date : datetime, optional
            The end time of the scheduled job. Must be a valid `datetime` object if provided.

        Raises
        ------
        CLIOrionisScheduleException
            If `start_date` or `end_date` are not valid `datetime` objects.
            If `start_date` is later than or equal to `end_date`.
        """

        # Ensure `start_date` is either None or a valid datetime object
        if start_date is not None and not isinstance(start_date, datetime):
            raise CLIOrionisScheduleException("start_date must be a valid datetime object.")

        # Ensure `end_date` is either None or a valid datetime object
        if end_date is not None and not isinstance(end_date, datetime):
            raise CLIOrionisScheduleException("end_date must be a valid datetime object.")

        # Ensure `start_date` is earlier than `end_date` if both are provided
        if start_date and end_date and start_date >= end_date:
            raise CLIOrionisScheduleException("start_date must be earlier than end_date.")

    def _checkGreterThanZero(self, value: int, identifier: str = 'interval'):
        """
        Validates that the value is greater than 0.
        """
        if value < 1:
            raise CLIOrionisScheduleException(f"The {identifier} must be greater than 0.")

    def onceAt(self, date: datetime):
        """
        Schedule the defined command to execute every X seconds.
        """
        self._checkCommand()

        if not isinstance(date, datetime):
            raise CLIOrionisScheduleException("The date must be a valid datetime object.")

        self.scheduler.add_job(
            self.callback,
            'date',
            run_date=date
        )

        self._resetCallback()

    def everySeconds(self, seconds: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedule the defined command to execute every X seconds.
        """
        self._checkCommand()
        self._checkGreterThanZero(seconds)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            IntervalTrigger(seconds=seconds, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def everySecond(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every second.
        """
        self.everySeconds(seconds=1, start_date=start_date, end_date=end_date)

    def everyTwoSeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every two seconds.
        """
        self.everySeconds(seconds=2, start_date=start_date, end_date=end_date)

    def everyFiveSeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every five seconds.
        """
        self.everySeconds(seconds=5, start_date=start_date, end_date=end_date)

    def everyTenSeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every ten seconds.
        """
        self.everySeconds(seconds=10, start_date=start_date, end_date=end_date)

    def everyFifteenSeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every fifteen seconds.
        """
        self.everySeconds(seconds=15, start_date=start_date, end_date=end_date)

    def everyTwentySeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every twenty seconds.
        """
        self.everySeconds(seconds=20, start_date=start_date, end_date=end_date)

    def everyThirtySeconds(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every thirty seconds.
        """
        self.everySeconds(seconds=30, start_date=start_date, end_date=end_date)

    def everyMinutes(self, minutes: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every X minutes.
        """
        self._checkCommand()
        self._checkGreterThanZero(minutes)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            IntervalTrigger(minutes=minutes, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def everyMinute(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every minute.
        """
        self.everyMinutes(minutes=1, start_date=start_date, end_date=end_date)

    def everyTwoMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every two minutes.
        """
        self.everyMinutes(minutes=2, start_date=start_date, end_date=end_date)

    def everyThreeMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every three minutes.
        """
        self.everyMinutes(minutes=3, start_date=start_date, end_date=end_date)

    def everyFourMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every four minutes.
        """
        self.everyMinutes(minutes=4, start_date=start_date, end_date=end_date)

    def everyFiveMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every five minutes.
        """
        self.everyMinutes(minutes=5, start_date=start_date, end_date=end_date)

    def everyTenMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every ten minutes.
        """
        self.everyMinutes(minutes=10, start_date=start_date, end_date=end_date)

    def everyFifteenMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every fifteen minutes.
        """
        self.everyMinutes(minutes=15, start_date=start_date, end_date=end_date)

    def everyThirtyMinutes(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every thirty minutes.
        """
        self.everyMinutes(minutes=30, start_date=start_date, end_date=end_date)

    def hours(self, hours: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every X hours.
        """
        self._checkCommand()
        self._checkGreterThanZero(hours)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            IntervalTrigger(hours=hours, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def hourly(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every hour.
        """
        self.hours(hours=1, start_date=start_date, end_date=end_date)

    def hourlyAt(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every hour at a specific minute.
        """
        self._checkCommand()
        self._checkGreterThanZero(minute)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='*', minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def everyOddHour(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every odd hour.
        """
        self._checkCommand()
        self._checkGreterThanZero(minute)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='1,3,5,7,9,11,13,15,17,19,21,23', minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def everyTwoHours(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every two hours.
        """
        self._checkCommand()
        self._checkGreterThanZero(minute)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='*/2', minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def everyThreeHours(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every three hours.
        """
        self._checkCommand()
        self._checkGreterThanZero(minute)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='*/3', minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def everyFourHours(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every four hours.
        """
        self._checkCommand()
        self._checkGreterThanZero(minute)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='*/4', minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def everySixHours(self, minute: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every six hours.
        """
        self._checkCommand()
        self._checkGreterThanZero(minute)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='*/6', minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def days(self, days: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every X days.
        """
        self._checkCommand()
        self._checkGreterThanZero(days)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            IntervalTrigger(days=days, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def daily(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute daily at midnight.
        """
        self._checkCommand()
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour=0, minute=0, second=1, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def dailyAt(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute daily at a specific time.
        """
        self._checkCommand()
        self._checkDateTime(start_date, end_date)
        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour=hour, minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def twiceDaily(self, first_hour: int, second_hour: int, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute twice a day at specific hours.
        """
        self._checkCommand()
        self._checkGreterThanZero(first_hour)
        self._checkGreterThanZero(second_hour)
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour=f'{first_hour},{second_hour}', minute=0, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def monday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every Monday at a specific time.
        """

        self._checkCommand()
        self._checkDateTime(start_date, end_date)
        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='mon', hour=hour, minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def tuesday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every tuesday at a specific time.
        """

        self._checkCommand()
        self._checkDateTime(start_date, end_date)
        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='tue', hour=hour, minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def wednesday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every wednesday at a specific time.
        """

        self._checkCommand()
        self._checkDateTime(start_date, end_date)
        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='wed', hour=hour, minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def thursday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every thursday at a specific time.
        """

        self._checkCommand()
        self._checkDateTime(start_date, end_date)
        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='thu', hour=hour, minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def friday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every friday at a specific time.
        """

        self._checkCommand()
        self._checkDateTime(start_date, end_date)
        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='fri', hour=hour, minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def saturday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every saturday at a specific time.
        """

        self._checkCommand()
        self._checkDateTime(start_date, end_date)
        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='sat', hour=hour, minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def sunday(self, at: str, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute every sunday at a specific time.
        """

        self._checkCommand()
        self._checkDateTime(start_date, end_date)
        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='sun', hour=hour, minute=minute, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def weekly(self, start_date: datetime = None, end_date: datetime = None):
        """
        Schedules the defined command to execute weekly on Sunday at midnight.
        """

        self._checkCommand()
        self._checkDateTime(start_date, end_date)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='sun', hour=0, minute=0, second=1, start_date=start_date, end_date=end_date),
            replace_existing=True
        )

        self._resetCallback()

    def start(self):
        """
        Starts the scheduler and stops automatically when there are no more jobs.
        """
        try:
            # Start the scheduler
            while self.wait:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            # Stop the scheduler if it is running
            if self.scheduler.running:
                self.scheduler.shutdown()
            # Exit with status code 1 to indicate an error
            sys.exit(1)