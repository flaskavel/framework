from test import handle_test_framework
from flaskavel.luminate.publisher.pypi import PypiPublisher
from flaskavel.luminate.test.exception import FlaskavelTestFailureException

# Ensures that the script runs only when executed directly,
def handle_publishing_framework():

    # Import the test module to ensure all tests pass before publishing
    publisher = PypiPublisher()

    # Publish the package
    publisher.gitPush()

    # Build the package
    publisher.build()

    # Publish the package
    publisher.publish()

if __name__ == "__main__":
    """
    Main execution script for managing the package publishing process.

    This script performs the following actions in sequence:
    1. Initializes the `PypiPublisher` instance.
    2. Cleans up the repository by removing temporary files.
    3. Commits and pushes changes to the Git repository.
    4. Publishes the package to PyPI.
    5. Performs a final cleanup of temporary files.

    Raises
    ------
    ValueError
        If any exception occurs during the publishing process,
        it is caught and raised as a `ValueError` with a descriptive message.
    """
    try:

        # Import the test module to ensure all tests pass before publishing
        result = handle_test_framework()

        if result.get('failures') > 0 or result.get('errors') > 0:
            raise FlaskavelTestFailureException("Tests failed. Publishing aborted.")

        # Run the publishing framework when the script is executed directly.
        handle_publishing_framework()

    except Exception as e:

        # Raise a general error if the exception is not a test failure exception
        if not type(e) is FlaskavelTestFailureException:
            raise ValueError(f"General Error: {e}")
