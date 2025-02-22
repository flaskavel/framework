from orionis.contracts.facades.environment.i_environment_facade import IEnv
from orionis.luminate.app_context import AppContext

def env(key: str, default=None) -> str:
    """
    Retrieves the value of an environment variable.

    This function provides a convenient way to access environment variables
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
    with AppContext() as app:
        env : dict = app._environment_vars
        return env.get(key, default)

class Env(IEnv):
    """
    A facade class for accessing environment variables.

    This class provides a static method to retrieve environment variables
    stored in the application context. It implements the `IEnv` interface.

    Methods
    -------
    get(key: str, default=None) -> str
        Retrieves the value of an environment variable.
    """

    @staticmethod
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
        with AppContext() as app:
            env : dict = app._environment_vars
            return env.get(key, default)