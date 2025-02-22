from orionis.luminate.support.environment import Environment

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