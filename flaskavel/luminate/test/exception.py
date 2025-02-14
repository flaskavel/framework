class FlaskavelTestFailureException(Exception):
    """
    Custom exception raised when test execution results in one or more failures.

    This exception is used to indicate that a test suite run has encountered failures.
    It stores a response message detailing the number of failed tests or other relevant
    error information.

    Parameters
    ----------
    response : str
        A message describing the reason for the test failure.

    Attributes
    ----------
    response : str
        Stores the response message describing the failure.

    Methods
    -------
    __str__() -> str
        Returns a string representation of the exception, including the response message.
    """

    def __init__(self, response: str):
        """
        Initializes the exception with a response message.

        Parameters
        ----------
        response : str
            The message describing the test failure.
        """
        self.response = response
        super().__init__(response)  # Ensures proper initialization of the Exception class

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the exception.

        Returns
        -------
        str
            A formatted string containing the exception name and response message.
        """
        return f"FlaskavelTestFailureException: {self.response}"
