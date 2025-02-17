from abc import ABC, abstractmethod

class IExecutor(ABC):
    """
    Interface for execution state logging.

    This interface defines methods for logging different execution states:
    "RUNNING", "DONE", and "FAIL".
    """

    @abstractmethod
    def running(program: str, time: str = ''):
        """
        Logs the execution of a program in a "RUNNING" state.

        Parameters
        ----------
        program : str
            The name of the program being executed.
        time : str, optional
            The time duration of execution, default is an empty string.
        """
        pass

    @abstractmethod
    def done(program: str, time: str = ''):
        """
        Logs the execution of a program in a "DONE" state.

        Parameters
        ----------
        program : str
            The name of the program being executed.
        time : str, optional
            The time duration of execution, default is an empty string.
        """
        pass

    @abstractmethod
    def fail(program: str, time: str = ''):
        """
        Logs the execution of a program in a "FAIL" state.

        Parameters
        ----------
        program : str
            The name of the program being executed.
        time : str, optional
            The time duration of execution, default is an empty string.
        """
        pass
