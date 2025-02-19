class CLIOrionisException(Exception):
    """
    Custom exception raised when there is an issue with dumping the Orionis data.

    Parameters
    ----------
    response : str
        The response message associated with the exception.

    Attributes
    ----------
    response : str
        Stores the response message passed during initialization.

    Methods
    -------
    __str__()
        Returns a string representation of the exception, including the response message.
    """

    def __init__(self, response: str):
        """
        Initializes the CLIOrionisException with the given response message.

        Parameters
        ----------
        response : str
            The response message associated with the exception.
        """
        self.response = response

    def __str__(self):
        """
        Returns a string representation of the exception, including the response message.

        Returns
        -------
        str
            A string containing the exception name and the response message.
        """
        return f"[CLIOrionisException]: {self.response}"

class CLIOrionisValueError(ValueError):
    """
    Custom exception raised when there is an issue with dumping the Orionis data.

    Parameters
    ----------
    response : str
        The response message associated with the exception.

    Attributes
    ----------
    response : str
        Stores the response message passed during initialization.

    Methods
    -------
    __str__()
        Returns a string representation of the exception, including the response message.
    """

    def __init__(self, response: str):
        """
        Initializes the CLIOrionisValueError with the given response message.

        Parameters
        ----------
        response : str
            The response message associated with the exception.
        """
        self.response = response

    def __str__(self):
        """
        Returns a string representation of the exception, including the response message.

        Returns
        -------
        str
            A string containing the exception name and the response message.
        """
        return f"[CLIOrionisValueError]: {self.response}"

class CLIOrionisScheduleException(Exception):
    """
    Custom exception raised when there is an issue with dumping the Orionis data.

    Parameters
    ----------
    response : str
        The response message associated with the exception.

    Attributes
    ----------
    response : str
        Stores the response message passed during initialization.

    Methods
    -------
    __str__()
        Returns a string representation of the exception, including the response message.
    """

    def __init__(self, response: str):
        """
        Initializes the CLIOrionisScheduleException with the given response message.

        Parameters
        ----------
        response : str
            The response message associated with the exception.
        """
        self.response = response

    def __str__(self):
        """
        Returns a string representation of the exception, including the response message.

        Returns
        -------
        str
            A string containing the exception name and the response message.
        """
        return f"[CLIOrionisScheduleException]: {self.response}"