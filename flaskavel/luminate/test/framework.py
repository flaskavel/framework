import unittest
from flaskavel.luminate.console.output.console import Console
from flaskavel.luminate.test.exception import FlaskavelTestFailureException
from flaskavel.luminate.contracts.test.framework_interface import ITestFlaskavelFramework

class TestFlaskavelFramework(ITestFlaskavelFramework):
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

    def __init__(self) -> None:
        """
        Initializes the TestFlaskavelFramework class, setting up the test loader and suite.
        """
        self.loader = unittest.TestLoader()
        self.suite = unittest.TestSuite()

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
        try:
            tests = self.loader.discover(f"tests/{folder_path}", pattern=pattern)
            if not list(tests):  # Check if tests were found
                raise ValueError(f"No tests found in 'tests/{folder_path}' with pattern '{pattern}'.")
            self.suite.addTests(tests)
        except Exception as e:
            raise ValueError(f"Error discovering tests in 'tests/{folder_path}': {e}")

    def run(self) -> None:
        """
        Runs all tests added to the test suite.

        Raises
        ------
        FlaskavelTestFailureException
            If one or more tests fail.
        """

        # Display a message indicating that the tests are running
        Console.newLine()
        Console.info("Running Flaskavel Framework tests...")

        # Run the test suite and capture the results
        runner = unittest.TextTestRunner()
        result = runner.run(self.suite)

        # Check if any tests failed
        if result.failures:
            Console.error(f"{len(result.failures)} test(s) failed.")
            raise FlaskavelTestFailureException(f"{len(result.failures)} test(s) failed.")

        # Display a success message if all tests passed
        Console.success("All tests passed successfully.")
        Console.newLine()
