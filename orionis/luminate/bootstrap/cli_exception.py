class BootstrapRuntimeError(RuntimeError):
    """
    Exception raised for errors related to dumping Orionis data.

    Parameters
    ----------
    message : str
        The error message describing the issue.

    Attributes
    ----------
    message : str
        The stored error message.

    Methods
    -------
    __str__()
        Returns a user-friendly string representation of the exception.
    __repr__()
        Returns a detailed representation for debugging purposes.
    """

    def __init__(self, message: str):
        """
        Initialize the exception with a message.

        Parameters
        ----------
        message : str
            The error message describing the issue.
        """
        super().__init__(f"[BootstrapRuntimeError]: {message}")

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation.

        Returns
        -------
        str
            A formatted error message.
        """
        return self.args[0]

    def __repr__(self) -> str:
        """
        Returns a detailed representation for debugging.

        Returns
        -------
        str
            A detailed string representation including the exception name.
        """
        return f"{self.__class__.__name__}({self.args[0]!r})"
