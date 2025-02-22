import io
import re
import unittest
from contextlib import redirect_stdout
from orionis.luminate.console.output.console import Console

class UnitTest:
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
        Initializes the TestOrionisFramework class, setting up the test loader and suite.
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
        self.loader.discover(f"tests", pattern=pattern)

        try:
            tests = self.loader.discover(f"tests/{folder_path}", pattern=pattern)
            if not list(tests):  # Check if tests were found
                raise ValueError(f"No tests found in 'tests/{folder_path}' with pattern '{pattern}'.")
            self.suite.addTests(tests)
        except Exception as e:
            raise ValueError(f"Error discovering tests in 'tests/{folder_path}': {e}")

    def extract_error_file(self, traceback: str) -> str:
        """Extracts the file path from a traceback message."""
        match = re.search(r'File "([^"]+)"', traceback)
        return match.group(1) if match else None

    def run(self) -> dict:
        """
        Runs all tests added to the test suite.

        Raises
        ------
        OrionisTestFailureException
            If one or more tests fail.
        """
        Console.newLine()
        Console.info("Running Tests... 🔍")
        Console.newLine()

        # Capture output safely
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            runner = unittest.TextTestRunner(stream=output_buffer, verbosity=2)
            result = runner.run(self.suite)

        # Display summary table
        summary = {
            "tests": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors)
        }
        Console.table(headers=summary.keys(), rows=[summary.values()])
        Console.newLine()

        # Display failure details
        if result.failures:
            for test_case, traceback in result.failures:
                title = self.extract_error_file(traceback) or "Error in test"
                Console.fail(title)
                Console.write(traceback)

            Console.error(f"{summary['Failures']} test(s) failed.")
            Console.newLine()

        else:
            Console.success("All tests passed successfully.")
            Console.newLine()

        # Return summary
        return summary