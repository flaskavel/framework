from abc import ABC, abstractmethod

class IUnitTest(ABC):
    """
    A testing framework for discovering and running unit tests in a structured way.

    Attributes
    ----------
    loader : unittest.TestLoader
        A test loader instance used to discover tests.
    suite : unittest.TestSuite
        A test suite that holds all discovered tests.

    Methods
    -------
    add_folder_tests(folder_path: str, pattern: str = 'test_*.py') -> None
        Adds test cases from a specified folder to the test suite.
    run_tests() -> None
        Executes all tests in the test suite and raises an exception if any fail.
    """

    @abstractmethod
    def addFolderTests(self, folder_path: str, pattern: str = "test_*.py") -> None:
        """
        Adds all test cases from a specified folder to the test suite.

        Parameters
        ----------
        folder_path : str
            The relative path to the folder containing test files.
        pattern : str, optional
            A pattern to match test files (default is 'test_*.py').

        Raises
        ------
        ValueError
            If the folder path is invalid or no tests are found.
        """
        pass

    @abstractmethod
    def run(self) -> None:
        """
        Runs all tests added to the test suite.

        Raises
        ------
        OrionisTestFailureException
            If one or more tests fail.
        """
        pass
