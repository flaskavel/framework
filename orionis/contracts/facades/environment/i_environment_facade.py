
from abc import ABC, abstractmethod

class IEnv(ABC):
    """
    A facade class for accessing environment variables.

    This class provides a static method to retrieve environment variables
    stored in the application context. It implements the `IEnv` interface.

    Methods
    -------
    get(key: str, default=None) -> str
        Retrieves the value of an environment variable.
    """

    @abstractmethod
    def get(key: str, default=None) -> str:
        """
        Retrieves the value of an environment variable.

        This method provides a convenient way to access environment variables
        stored in the application context. If the variable does not exist, it
        returns the specified default value.

        Parameters
        ----------
        key : str
            The name of the environment variable to retrieve.
        default : Any, optional
            The default value to return if the environment variable does not exist.
            Defaults to None.

        Returns
        -------
        str
            The value of the environment variable, or the default value if the variable
            does not exist.
        """
        pass