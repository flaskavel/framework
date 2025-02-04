from flaskavel.lab.catalyst.environment import _Environment

def env(key: str, default=None):
    """
    Retrieves the value of an environment variable and converts it to a boolean
    if it represents 'true' or 'false' (case-insensitive).

    Args:
        key (str): The key for the environment variable.
        default: The default value if the environment variable is not found.

    Returns:
        The processed value of the environment variable or the default value.
        If the value is 'True'/'true' or 'False'/'false', it is converted to a boolean.
    """
    value = Env.get(key, default)

    if isinstance(value, str) and value.lower() == 'true':
        return True
    elif isinstance(value, str) and value.lower() == 'false':
        return False

    return value

class Env:
    """
    The Env class provides static methods to manage environment variables,
    allowing for setting, retrieving, and removing them, along with accessing
    all environment variable values and the .env file path.
    """

    @staticmethod
    def get(key: str, default=None):
        """
        Static method to retrieve the value of an environment variable.

        Args:
            key (str): The key of the environment variable.
            default: The default value if the key does not exist.

        Returns:
            The value of the environment variable or the default value if not found.
        """
        environment = _Environment()
        return environment.get(key=key, default=default)

    @staticmethod
    def set(key: str, value: str):
        """
        Static method to set the value of an environment variable.

        Args:
            key (str): The key of the environment variable.
            value (str): The value to assign.

        Returns:
            None
        """
        environment = _Environment()
        environment.set(key=key, value=value)

    @staticmethod
    def unset(key: str):
        """
        Static method to remove an environment variable.

        Args:
            key (str): The key of the environment variable to remove.

        Returns:
            None
        """
        environment = _Environment()
        environment.unset(key=key)

    @staticmethod
    def get_values():
        """
        Static method to retrieve all environment variable values.

        Returns:
            dict: A dictionary containing all environment variables and their values.
        """
        environment = _Environment()
        return environment.get_values()

    @staticmethod
    def get_path():
        """
        Static method to retrieve the path of the .env file.

        Returns:
            str: The path to the .env file.
        """
        environment = _Environment()
        return environment.get_path()
