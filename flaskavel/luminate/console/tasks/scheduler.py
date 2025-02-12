import re
import time
import logging
from typing import Any
from apscheduler.triggers.cron import CronTrigger
from flaskavel.luminate.console.command import Command
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from flaskavel.luminate.console.exceptions.cli_exception import CLIFlaskavelScheduleException

class Schedule:
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

    def command(self, signature: str, vars: dict[str, Any] = {}, *args: Any, **kwargs: Any) -> 'Schedule':
        """
        Defines a Flaskavel command to be executed.

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
        # Store the command logic as a lambda function
        self.callback = lambda: Command.call(signature, vars, *args, **kwargs)
        return self

    def _checkCommand(self):
        """
        Raises an exception to test the exception handling in the CLI.
        """
        if not self.callback:
            raise CLIFlaskavelScheduleException("No command has been defined to execute.")

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
            raise CLIFlaskavelScheduleException("Time must be a string in 'HH:MM' format. Example: '23:59'.")

        # Regular expression for the "HH:MM" 24-hour format
        pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"

        if not re.match(pattern, at):
            raise CLIFlaskavelScheduleException("Invalid time format. Expected 'HH:MM' (24-hour format). Example: '23:59'.")

        return at.split(':')

    def everySeconds(self, seconds: int):
        """
        Schedule the defined command to execute every X seconds.
        """
        self._checkCommand()

        if seconds < 1:
            raise CLIFlaskavelScheduleException("The interval must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            IntervalTrigger(seconds=seconds),
            replace_existing=True
        )

        self._resetCallback()

    def everySecond(self):
        """
        Schedules the defined command to execute every second.
        """
        self.everySeconds(1)

    def everyTwoSeconds(self):
        """
        Schedules the defined command to execute every two seconds.
        """
        self.everySeconds(2)

    def everyFiveSeconds(self):
        """
        Schedules the defined command to execute every five seconds.
        """
        self.everySeconds(5)

    def everyTenSeconds(self):
        """
        Schedules the defined command to execute every ten seconds.
        """
        self.everySeconds(10)

    def everyFifteenSeconds(self):
        """
        Schedules the defined command to execute every fifteen seconds.
        """
        self.everySeconds(15)

    def everyTwentySeconds(self):
        """
        Schedules the defined command to execute every twenty seconds.
        """
        self.everySeconds(20)

    def everyThirtySeconds(self):
        """
        Schedules the defined command to execute every thirty seconds.
        """
        self.everySeconds(30)

    def everyMinutes(self, minutes: int):
        """
        Schedules the defined command to execute every X minutes.
        """
        self._checkCommand()

        if minutes < 1:
            raise CLIFlaskavelScheduleException("The interval must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            IntervalTrigger(minutes=minutes),
            replace_existing=True
        )

        self._resetCallback()

    def everyMinute(self):
        """
        Schedules the defined command to execute every minute.
        """
        self.everyMinutes(1)

    def everyTwoMinutes(self):
        """
        Schedules the defined command to execute every two minutes.
        """
        self.everyMinutes(2)

    def everyThreeMinutes(self):
        """
        Schedules the defined command to execute every three minutes.
        """
        self.everyMinutes(3)

    def everyFourMinutes(self):
        """
        Schedules the defined command to execute every four minutes.
        """
        self.everyMinutes(4)

    def everyFiveMinutes(self):
        """
        Schedules the defined command to execute every five minutes.
        """
        self.everyMinutes(5)

    def everyTenMinutes(self):
        """
        Schedules the defined command to execute every ten minutes.
        """
        self.everyMinutes(10)

    def everyFifteenMinutes(self):
        """
        Schedules the defined command to execute every fifteen minutes.
        """
        self.everyMinutes(15)

    def everyThirtyMinutes(self):
        """
        Schedules the defined command to execute every thirty minutes.
        """
        self.everyMinutes(30)

    def hours(self, hours: int):
        """
        Schedules the defined command to execute every X hours.
        """
        self._checkCommand()

        if hours < 1:
            raise CLIFlaskavelScheduleException("The interval must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            IntervalTrigger(hours=hours),
            replace_existing=True
        )

        self._resetCallback()

    def hourly(self):
        """
        Schedules the defined command to execute every hour.
        """
        self.hours(1)

    def hourlyAt(self, minute: int):
        """
        Schedules the defined command to execute every hour at a specific minute.
        """
        self._checkCommand()

        if minute < 1:
            raise CLIFlaskavelScheduleException("The minute must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='*', minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def everyOddHour(self, minute: int):
        """
        Schedules the defined command to execute every odd hour.
        """
        self._checkCommand()

        if minute < 1:
            raise CLIFlaskavelScheduleException("The minute must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='1,3,5,7,9,11,13,15,17,19,21,23', minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def everyTwoHours(self, minute: int):
        """
        Schedules the defined command to execute every two hours.
        """
        self._checkCommand()

        if minute < 1:
            raise CLIFlaskavelScheduleException("The minute must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='*/2', minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def everyThreeHours(self, minute: int):
        """
        Schedules the defined command to execute every three hours.
        """
        self._checkCommand()

        if minute < 1:
            raise CLIFlaskavelScheduleException("The minute must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='*/3', minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def everyFourHours(self, minute: int):
        """
        Schedules the defined command to execute every four hours.
        """
        self._checkCommand()

        if minute < 1:
            raise CLIFlaskavelScheduleException("The minute must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='*/4', minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def everySixHours(self, minute: int):
        """
        Schedules the defined command to execute every six hours.
        """
        self._checkCommand()

        if minute < 1:
            raise CLIFlaskavelScheduleException("The minute must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour='*/6', minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def days(self, days: int):
        """
        Schedules the defined command to execute every X days.
        """
        self._checkCommand()

        if days < 1:
            raise CLIFlaskavelScheduleException("The days must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            IntervalTrigger(days=days),
            replace_existing=True
        )

        self._resetCallback()

    def daily(self):
        """
        Schedules the defined command to execute daily at midnight.
        """
        self._checkCommand()

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour=0, minute=0, second=1),
            replace_existing=True
        )

        self._resetCallback()

    def dailyAt(self, at: str):
        """
        Schedules the defined command to execute daily at a specific time.
        """
        self._checkCommand()

        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour=hour, minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def twiceDaily(self, first_hour: int, second_hour: int):
        """
        Schedules the defined command to execute twice a day at specific hours.
        """
        self._checkCommand()

        if first_hour < 1:
            raise CLIFlaskavelScheduleException("The first hour must be greater than 0.")

        if second_hour < 1:
            raise CLIFlaskavelScheduleException("The second hour must be greater than 0.")

        self.scheduler.add_job(
            self.callback,
            CronTrigger(hour=f'{first_hour},{second_hour}', minute=0),
            replace_existing=True
        )

        self._resetCallback()

    def monday(self, at: str):
        """
        Schedules the defined command to execute every Monday at a specific time.
        """

        self._checkCommand()

        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='mon', hour=hour, minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def tuesday(self, at: str):
        """
        Schedules the defined command to execute every tuesday at a specific time.
        """

        self._checkCommand()

        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='tue', hour=hour, minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def wednesday(self, at: str):
        """
        Schedules the defined command to execute every wednesday at a specific time.
        """

        self._checkCommand()

        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='wed', hour=hour, minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def thursday(self, at: str):
        """
        Schedules the defined command to execute every thursday at a specific time.
        """

        self._checkCommand()

        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='thu', hour=hour, minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def friday(self, at: str):
        """
        Schedules the defined command to execute every friday at a specific time.
        """

        self._checkCommand()

        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='fri', hour=hour, minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def saturday(self, at: str):
        """
        Schedules the defined command to execute every saturday at a specific time.
        """

        self._checkCommand()

        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='sat', hour=hour, minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def sunday(self, at: str):
        """
        Schedules the defined command to execute every sunday at a specific time.
        """

        self._checkCommand()

        hour, minute = self._hourFormat(at)

        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='sun', hour=hour, minute=minute),
            replace_existing=True
        )

        self._resetCallback()

    def weekly(self):
        """
        Schedules the defined command to execute weekly on Sunday at midnight.
        """
        self.scheduler.add_job(
            self.callback,
            CronTrigger(day_of_week='sun', hour=0, minute=0, second=1),
            replace_existing=True
        )
        self.callback = None

    def start(self):
        """
        Keeps the scheduler running in the background.

        This method will run an infinite loop to keep the scheduler active.
        It will stop when a KeyboardInterrupt or SystemExit exception is raised.
        """
        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()
