from abc import ABC, abstractmethod

class IUnitTests(ABC):
    """
    Interface for executing unit tests based on a specified pattern.

    Methods
    -------
    execute(pattern: str) -> dict
        Executes unit tests by iterating over the 'tests' directory and its subdirectories,
        matching test files based on the provided pattern.
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
