import sys
from orionis.luminate.contracts.console.output.progress_bar_interface import IProgressBar

class ProgressBar(IProgressBar):
    """
    A console-based progress bar implementation.

    This class provides a simple text-based progress bar that updates
    in place without clearing the console.

    Parameters
    ----------
    total : int, optional
        The total amount of progress (default is 100).
    width : int, optional
        The width of the progress bar in characters (default is 50).

    Attributes
    ----------
    total : int
        The maximum progress value.
    bar_width : int
        The width of the progress bar in characters.
    progress : int
        The current progress value.

    Methods
    -------
    start()
        Initializes the progress bar to the starting state.
    advance(increment=1)
        Advances the progress bar by a given increment.
    finish()
        Completes the progress bar and moves to a new line.
    """

    def __init__(self, total=100, width=50):
        """
        Constructs all the necessary attributes for the progress bar object.

        Parameters
        ----------
        total : int, optional
            The total amount of progress (default is 100).
        width : int, optional
            The width of the progress bar in characters (default is 50).
        """
        self.total = total
        self.bar_width = width
        self.progress = 0

    def _update_bar(self):
        """
        Updates the visual representation of the progress bar.

        This method calculates the percentage of progress and updates the
        console output accordingly.
        """
        percent = self.progress / self.total
        filled_length = int(self.bar_width * percent)
        bar = f"[{'█' * filled_length}{'░' * (self.bar_width - filled_length)}] {int(percent * 100)}%"

        # Move the cursor to the start of the line and overwrite it
        sys.stdout.write("\r" + bar)
        sys.stdout.flush()

    def start(self):
        """
        Initializes the progress bar to the starting state.

        This method resets the progress to zero and displays the initial bar.
        """
        self.progress = 0
        self._update_bar()

    def advance(self, increment=1):
        """
        Advances the progress bar by a specific increment.

        Parameters
        ----------
        increment : int, optional
            The amount by which the progress should be increased (default is 1).
        """
        self.progress += increment
        if self.progress > self.total:
            self.progress = self.total
        self._update_bar()

    def finish(self):
        """
        Completes the progress bar.

        This method sets the progress to its maximum value, updates the bar,
        and moves the cursor to a new line for cleaner output.
        """
        self.progress = self.total
        self._update_bar()
        sys.stdout.write("\n")
        sys.stdout.flush()
