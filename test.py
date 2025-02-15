from flaskavel.luminate.facades.tests import UnitTests

def handle_test_framework() -> dict:
    """
    Executes the test framework using the UnitTest facade.

    This function serves as a wrapper to execute the UnitTests with the default settings.

    Returns:
    - dict: The results of the executed tests.
    """
    return UnitTests.execute(pattern="test_*.py")

if __name__ == "__main__":
    """
    Ensures the script runs only when executed directly.

    This condition prevents the script from executing when it is imported as a module
    into another script.
    """
    handle_test_framework()
