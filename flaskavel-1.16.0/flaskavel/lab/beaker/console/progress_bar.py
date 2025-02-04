import os
import sys
import platform

class ProgressBar:
    """
    Class to create and update a progress bar in the console.
    """

    def __init__(self, total=100, width=50, inline=False):
        """
        Initializes the progress bar.

        Args:
            total (int): The total amount of progress (default is 100).
            width (int, optional): The width of the progress bar in characters (default is 50).
            inline (bool, optional): Whether to clear the console or update the bar inline (default is False).
        """
        self.total = total
        self.bar_width = width
        self.progress = 0
        self.inline = inline

    def _update_bar(self):
        """
        Updates the visual representation of the progress bar.
        """
        if self.inline:
            # Clear the console depending on the operating system
            os.system('cls') if platform.system() == 'Windows' else os.system('clear')

        # Calculate the percentage of progress and the length of the filled part of the bar
        percent = self.progress / self.total
        filled_length = int(self.bar_width * percent)
        bar = f"[{'█' * filled_length}{'░' * (self.bar_width - filled_length)}] {int(percent * 100)}% : {self.progress}/{self.total}"

        # Move the cursor to the start of the current line and update the bar
        sys.stdout.write("\r" + bar)
        sys.stdout.flush()
        sys.stdout.write("\n")

    def start(self):
        """
        Initializes the progress bar to the starting state.
        """
        self.progress = 0
        self._update_bar()

    def advance(self, increment=1):
        """
        Advances the progress bar by a specific increment.

        Args:
            increment (int): The amount to advance in each update (default is 1).
        """
        self.progress += increment
        if self.progress > self.total:
            self.progress = self.total
        self._update_bar()

    def finish(self):
        """
        Completes the progress bar.
        """
        self.progress = self.total
        self._update_bar()
        sys.stdout.write("\n")
        sys.stdout.flush()
