import time
import schedule
from flaskavel.lab.beaker.console.reactor import reactor
from flaskavel.lab.catalyst.threaded import ConsoleThread

class Schedule:

    def command(self, signature: str, args: dict = {}):
        """
        Sets the command signature to be executed.

        Args:
            signature (str): The command signature.
        """
        self.signature = str(signature).strip()
        self.args = []

        # Create Arguments.
        if len(args) > 0:
            for key, value in args.items():
                if ' ' in str(value):
                    self.args.append(f'--{key}="{value}"')
                else:
                    self.args.append(f'--{key}={value}')

        return self

    def runner(self):
        """
        Continuously runs the scheduled tasks.
        """
        while True:
            schedule.run_pending()
            time.sleep(1)

    def everySeconds(self, seconds:int):
        """
        Schedule the task to run every ? seconds.
        """
        schedule.every(seconds).seconds.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everySecond(self):
        """
        Schedule the task to run every second.
        """
        schedule.every(1).seconds.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyTwoSeconds(self):
        """
        Schedule the task to run every two seconds.
        """
        schedule.every(2).seconds.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyFiveSeconds(self):
        """
        Schedule the task to run every five seconds.
        """
        schedule.every(5).seconds.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyTenSeconds(self):
        """
        Schedule the task to run every ten seconds.
        """
        schedule.every(10).seconds.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyFifteenSeconds(self):
        """
        Schedule the task to run every fifteen seconds.
        """
        schedule.every(15).seconds.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyTwentySeconds(self):
        """
        Schedule the task to run every twenty seconds.
        """
        schedule.every(20).seconds.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyThirtySeconds(self):
        """
        Schedule the task to run every thirty seconds.
        """
        schedule.every(30).seconds.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyMinutes(self, minutes:int):
        """
        Schedule the task to run every ? minutes.
        """
        schedule.every(minutes).minutes.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyMinute(self):
        """
        Schedule the task to run every minute.
        """
        schedule.every(1).minutes.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyTwoMinutes(self):
        """
        Schedule the task to run every two minutes.
        """
        schedule.every(2).minutes.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyThreeMinutes(self):
        """
        Schedule the task to run every three minutes.
        """
        schedule.every(3).minutes.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyFourMinutes(self):
        """
        Schedule the task to run every four minutes.
        """
        schedule.every(4).minutes.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyFiveMinutes(self):
        """
        Schedule the task to run every five minutes.
        """
        schedule.every(5).minutes.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyTenMinutes(self):
        """
        Schedule the task to run every ten minutes.
        """
        schedule.every(10).minutes.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyFifteenMinutes(self):
        """
        Schedule the task to run every fifteen minutes.
        """
        schedule.every(15).minutes.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyThirtyMinutes(self):
        """
        Schedule the task to run every thirty minutes.
        """
        schedule.every(30).minutes.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def hours(self, hours:int):
        """
        Schedule the task to run every ? hours.
        """
        schedule.every(hours).hours.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def hourly(self):
        """
        Schedule the task to run every hour.
        """
        schedule.every(1).hours.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def hourlyAt(self, minute: int):
        """
        Schedule the task to run hourly at a specific minute.

        Args:
            minute (int): The minute to run the task.
        """
        if minute > 59:
            raise ValueError('The minutes can be a minimum of 0 and a maximum of 59')

        schedule.every().hour.at(f":{str(minute).zfill(2)}").do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyOddHour(self, minutes:int=0):
        """
        Schedule the task to run every odd hour.

        Args:
            minutes (int, optional): The minute to run the task. Defaults to 0.
        """
        if minutes > 59:
            raise ValueError('The minutes can be a minimum of 0 and a maximum of 59')

        for hour in range(1, 24, 2):
            schedule.every().day.at(f"{str(hour).zfill(2)}:{str(minutes).zfill(2)}").do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyTwoHours(self, minutes:int=0):
        """
        Schedule the task to run every two hours.

        Args:
            minutes (int, optional): The minute to run the task. Defaults to 0.
        """
        if minutes > 59:
            raise ValueError('The minutes can be a minimum of 0 and a maximum of 59')

        for hour in range(0, 24, 2):
            schedule.every().hour.at(f"{str(hour).zfill(0)}:{str(minutes).zfill(2)}").do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyThreeHours(self, minutes:int=0):
        """
        Schedule the task to run every Three hours.

        Args:
            minutes (int, optional): The minute to run the task. Defaults to 0.
        """
        if minutes > 59:
            raise ValueError('The minutes can be a minimum of 0 and a maximum of 59')

        for hour in range(0, 24, 3):
            schedule.every().hour.at(f"{str(hour).zfill(0)}:{str(minutes).zfill(2)}").do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everyFourHours(self, minutes:int=0):
        """
        Schedule the task to run every Four hours.

        Args:
            minutes (int, optional): The minute to run the task. Defaults to 0.
        """
        if minutes > 59:
            raise ValueError('The minutes can be a minimum of 0 and a maximum of 59')

        for hour in range(0, 24, 4):
            schedule.every().hour.at(f"{str(hour).zfill(0)}:{str(minutes).zfill(2)}").do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def everySixHours(self, minutes:int=0):
        """
        Schedule the task to run every Six hours.

        Args:
            minutes (int, optional): The minute to run the task. Defaults to 0.
        """
        if minutes > 59:
            raise ValueError('The minutes can be a minimum of 0 and a maximum of 59')

        for hour in range(0, 24, 6):
            schedule.every().hour.at(f"{str(hour).zfill(0)}:{str(minutes).zfill(2)}").do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def days(self, days:int):
        """
        Schedule the task to run every ? days.
        """
        schedule.every(days).days.do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))


    def daily(self):
        """
        Schedule the task to run daily at midnight.
        """
        schedule.every().day.at("00:00").do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def dailyAt(self, time: str):
        """
        Schedule the task to run daily at a specific time.

        Args:
            time (str): The time in HH:MM format.
        """
        schedule.every().day.at(time).do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def twiceDaily(self, first_hour:int, second_hour:int):
        """
        Schedule the task twice a day.

        Args:
            minutes (int, optional): The minute to run the task. Defaults to 0.
        """
        if not (0 <= first_hour <= 23) or not (0 <= second_hour <= 23):
            raise ValueError("Hours must be between 0 and 23.")

        for hour in [first_hour, second_hour]:
            schedule.every().day.at(f"{str(hour).zfill(2)}:00").do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def twiceDailyAt(self, first_hour:int, second_hour:int, minutes:int=0):
        """
        Schedule the task twice a day with minutes.

        Args:
            minutes (int, optional): The minute to run the task. Defaults to 0.
        """
        if not (0 <= first_hour <= 23) or not (0 <= second_hour <= 23):
            raise ValueError("Hours must be between 0 and 23.")
        if not (0 <= minutes <= 59):
            raise ValueError("Minutes must be between 0 and 59.")

        for hour in [first_hour, second_hour]:
            schedule.every().day.at(f"{str(hour).zfill(2)}:{str(minutes).zfill(2)}").do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def monday(self, at:str='00:00'):
        """
        Schedule the task to run every monday at 00:00.
        """
        schedule.every().monday.at(at).do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def tuesday(self, at:str='00:00'):
        """
        Schedule the task to run every tuesday at 00:00.
        """
        schedule.every().tuesday.at(at).do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def wednesday(self, at:str='00:00'):
        """
        Schedule the task to run every wednesday at 00:00.
        """
        schedule.every().wednesday.at(at).do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def thursday(self, at:str='00:00'):
        """
        Schedule the task to run every thursday at 00:00.
        """
        schedule.every().thursday.at(at).do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def friday(self, at:str='00:00'):
        """
        Schedule the task to run every friday at 00:00.
        """
        schedule.every().friday.at(at).do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def saturday(self, at:str='00:00'):
        """
        Schedule the task to run every saturday at 00:00.
        """
        schedule.every().saturday.at(at).do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def sunday(self, at:str='00:00'):
        """
        Schedule the task to run every sunday at 00:00.
        """
        schedule.every().sunday.at(at).do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))

    def weekly(self):
        """
        Schedule the task to run every Sunday at 00:00.
        """
        schedule.every().sunday.at("00:00").do(lambda: ConsoleThread().target(function=reactor.call).start(self.signature, self.args))
