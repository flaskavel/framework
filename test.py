import sys
import time

class ProgressBar:
    """
    Class to create and update a progress bar in the console.
    """

    def __init__(self, total=100, width=50):
        """
        Initializes the progress bar.

        Args:
            total (int): The total amount of progress (default is 100).
            width (int, optional): The width of the progress bar in characters (default is 50).
        """
        self.total = total
        self.bar_width = width
        self.progress = 0

    def _update_bar(self):
        """
        Updates the visual representation of the progress bar.
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
        sys.stdout.write("\n")  # Move to a new line after completion
        sys.stdout.flush()

print("Prueba")  # This will not be erased
progressbar = ProgressBar()
progressbar.start()
for _ in range(10):
    time.sleep(1)
    progressbar.advance(increment=10)
progressbar.finish()
print("Finalizado")  # Esto se imprimirá sin ser borrado
