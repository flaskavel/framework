from abc import ABC, abstractmethod

class IUnitTests(ABC):
    """
    Interface for executing unit tests in a specified directory.

    This class defines the abstract structure for any unit test executor,
    enforcing the implementation of the 'execute' method in any subclass.

    Methods
    -------
    execute(pattern: str) -> dict
        Executes the unit tests in the 'tests' directory and subdirectories,
        using a file pattern for filtering test files.
    """

    @abstractmethod
    def execute(pattern='test_*.py') -> dict:
        """
        Executes the unit tests in the 'tests' directory and its subdirectories
        by filtering test files based on a specified pattern.

        Parameters
        ----------
        pattern : str, optional
            The pattern to filter test files (default is 'test_*.py').

        Returns
        -------
        dict
            A dictionary containing the results of the executed tests.
        """
        pass
