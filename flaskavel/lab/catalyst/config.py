from flaskavel.lab.catalyst.bootstrap_cache import _BootstrapCache

class Config:
    """
    Provides a centralized access point for application configuration settings.

    The configuration is divided into predefined sections and supports
    accessing nested values via dot notation.
    """

    SECTIONS = ['app', 'auth', 'cache', 'cors', 'database', 'filesystems',
                'logging', 'mail', 'queue', 'session', 'bootstrap']  # Predefined config sections

    @staticmethod
    def get(section: str, dot_values: str = None):
        """
        Retrieves the specified configuration section or nested value.

        Args:
            section (str): The main configuration section to access.
            dot_values (str, optional): A dot-separated string indicating
                                        nested keys within the section.

        Returns:
            Any: The configuration value associated with the provided section/key.

        Raises:
            KeyError: If the section or nested key is not found in the configuration.
        """
        if section not in Config.SECTIONS:
            raise KeyError(f"The section '{section}' is not found in the configuration.")

        config_app = _BootstrapCache().get_config()  # Fetches full config data
        if not dot_values:
            return config_app.get(section)

        # Splits dot notation to navigate through nested config values
        data = dot_values.split('.')

        # Initialize index to point to the specific section within the config
        index = config_app.get(section)
        if index is None:
            raise KeyError(f"The section '{section}' is empty or not found in the configuration.")

        # Iteratively access nested keys in the config using dot notation
        for key in data:
            index = index.get(key)
            if index is None:
                raise KeyError(f"The key '{key}' is not found in the configuration under section '{section}'.")

        return index

    @staticmethod
    def app(value: str = None):
        """
        Accesses the 'app' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'app' section values.
        """
        return Config.get('app', value)

    @staticmethod
    def auth(value: str = None):
        """
        Accesses the 'auth' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'auth' section values.
        """
        return Config.get('auth', value)

    @staticmethod
    def cache(value: str = None):
        """
        Accesses the 'cache' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'cache' section values.
        """
        return Config.get('cache', value)

    @staticmethod
    def cors(value: str = None):
        """
        Accesses the 'cors' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'cors' section values.
        """
        return Config.get('cors', value)

    @staticmethod
    def database(value: str = None):
        """
        Accesses the 'database' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'database' section values.
        """
        return Config.get('database', value)

    @staticmethod
    def filesystems(value: str = None):
        """
        Accesses the 'filesystems' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'filesystems' section values.
        """
        return Config.get('filesystems', value)

    @staticmethod
    def logging(value: str = None):
        """
        Accesses the 'logging' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'logging' section values.
        """
        return Config.get('logging', value)

    @staticmethod
    def mail(value: str = None):
        """
        Accesses the 'mail' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'mail' section values.
        """
        return Config.get('mail', value)

    @staticmethod
    def queue(value: str = None):
        """
        Accesses the 'queue' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'queue' section values.
        """
        return Config.get('queue', value)

    @staticmethod
    def session(value: str = None):
        """
        Accesses the 'session' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'session' section values.
        """
        return Config.get('session', value)

    @staticmethod
    def bootstrap(value: str = None):
        """
        Accesses the 'bootstrap' section or a specific key within it.

        Args:
            value (str, optional): Dot notation key for nested 'bootstrap' section values.
        """
        return Config.get('bootstrap', value)
