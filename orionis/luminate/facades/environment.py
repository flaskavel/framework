from orionis.luminate.config.environment import Environment
from orionis.luminate.contracts.facades.env_interface import IEnv

def env(key: str, default=None) -> str:
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
    return Environment().get(key, default)

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
        Environment().get(key, default)

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
        Environment().set(key, value)

    @staticmethod
    def unset(key: str) -> None:
        """
        Removes an environment variable from the .env file.

        Parameters
        ----------
        key : str
            The key of the environment variable to remove.
        """
        Environment().unset(key)

    @staticmethod
    def all() -> dict:
        """
        Retrieves all environment variable values from the .env file.

        Returns
        -------
        dict
            A dictionary of all environment variables and their values.
        """
        Environment().all()