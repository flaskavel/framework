import os
from orionis.luminate.contracts.facades.tests.i_tests_facade import IUnitTests
from orionis.luminate.test.unit_test import UnitTest

class UnitTests(IUnitTests):
    """
    Concrete implementation of the IUnitTests interface.

    This class provides the functionality to execute unit tests using a specified pattern
    to filter test files within the 'tests' directory and its subdirectories.

    Methods
    -------
    execute(pattern: str) -> dict
        Executes unit tests by iterating over the 'tests' directory and its subdirectories,
        matching test files based on the provided pattern.
    """

    @staticmethod
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

        # Initialize the test suite using the UnitTest framework
        test_suite = UnitTest()

        # Define the base directory for test files
        tests_path = os.path.join(os.getcwd(), 'tests')

        # Recursively walk through the 'tests' directory
        for root, dirs, files in os.walk(tests_path):
            for dir in dirs:
                test_suite.addFolderTests(folder_path=dir, pattern=pattern)

        # Execute the tests and return the results
        return test_suite.run()
