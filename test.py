import unittest
from tests.tools.test_reflection import *

if __name__ == "__main__":

    # Create a test loader and test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Discover all test files (test_*.py) inside the 'tests/tools' folder
    suite.addTests(loader.discover('tests/tools', pattern='test_*.py'))

    # Create a test runner
    runner = unittest.TextTestRunner()

    # Run the tests
    runner.run(suite)
