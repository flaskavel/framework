from orionis.contracts.facades.environment.i_environment_facade import IEnv
from orionis.luminate.facades.app_facade import app
from orionis.luminate.services.environment.environment_service import EnvironmentService

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
    return Env.get(key, default)

class Env(IEnv):


    @staticmethod
    def get(key: str, default=None) -> str:
        """
        Retrieves the value of an environment variable from the .env file
        or from system environment variables if not found.

        Parameters
        ----------
        key : str
            The key of the environment variable.
        default : optional
            Default value if the key does not exist. Defaults to None.

        Returns
        -------
        str
            The value of the environment variable or the default value.
        """

        _env_service : EnvironmentService = app(EnvironmentService)
        return _env_service.get(key, default)

    @staticmethod
    def set(key: str, value: str) -> None:
        """
        Sets the value of an environment variable in the .env file.

        Parameters
        ----------
        key : str
            The key of the environment variable.
        value : str
            The value to set.
        """
        _env_service : EnvironmentService = app(EnvironmentService)
        return _env_service.set(key, value)

    @staticmethod
    def unset(key: str) -> None:
        """
        Removes an environment variable from the .env file.

        Parameters
        ----------
        key : str
            The key of the environment variable to remove.
        """
        _env_service : EnvironmentService = app(EnvironmentService)
        return _env_service.unset(key)

    @staticmethod
    def all() -> dict:
        """
        Retrieves all environment variable values from the .env file.

        Returns
        -------
        dict
            A dictionary of all environment variables and their values.
        """
        _env_service : EnvironmentService = app(EnvironmentService)
        return _env_service.all()