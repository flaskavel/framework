from abc import ABC, abstractmethod

class IProgressBar(ABC):
    """
    Interface for a progress bar.

    This interface defines the structure for a progress bar, enforcing
    the implementation of methods to initialize, update, and complete
    the progress tracking.

    Methods
    -------
    start()
        Initializes the progress bar and sets it to the starting state.
    advance(increment)
        Advances the progress bar by a specific increment.
    finish()
        Completes the progress bar and ensures the final state is displayed.
    """

    @abstractmethod
    def start(self):
        """
        Initializes the progress bar.

        This method should be implemented to set the progress bar
        to its initial state and display the starting progress.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a subclass.
        """
        pass

    @abstractmethod
    def advance(self, increment: int):
        """
        Advances the progress bar by a given increment.

        Parameters
        ----------
        increment : int
            The amount by which the progress should be increased.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a subclass.
        """
        pass

    @abstractmethod
    def finish(self):
        """
        Completes the progress bar.

        This method should be implemented to ensure the progress bar
        reaches its final state and is properly displayed.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a subclass.
        """
        pass
