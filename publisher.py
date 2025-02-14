from flaskavel.luminate.publisher.pypi import PypiPublisher
from test import run_tests

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
        run_tests()

        # Publish the package
        publisher = PypiPublisher()
        publisher.gitPush()
        publisher.build()
        publisher.publish()
    except Exception as e:
        raise ValueError(f"General Error: {e}")
