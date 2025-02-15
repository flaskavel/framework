from flaskavel.luminate.test.unit_test import UnitTest

# Ensures that the script runs only when executed directly,
# preventing it from running if imported as a module.

def handle_test_framework():

    # Initialize the test suite using the custom testing framework.
    test_suite = UnitTest()

    # Add test cases from the 'tools' folder that match the default pattern ('test_*.py').
    test_suite.addFolderTests('tools')

    # Execute the test suite and raise an exception if any test fails.
    return test_suite.run()

if __name__ == "__main__":

    # Run the test framework when the script is executed directly.
    handle_test_framework()