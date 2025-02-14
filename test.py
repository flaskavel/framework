import unittest
from tests.tools.test_reflection import *

def run_tests():
    # Create a test loader and test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Discover all test files (test_*.py) inside the 'tests/tools' folder
    suite.addTests(loader.discover('tests/tools', pattern='test_*.py'))

    # Create a test runner
    runner = unittest.TextTestRunner()

    # Run the tests
    result = runner.run(suite)

    # Check how many tests failed
    if len(result.failures) > 0:
        raise ValueError(f"{len(result.failures)} test(s) failed.")

if __name__ == "__main__":
    run_tests()
