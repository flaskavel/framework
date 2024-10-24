from flaskavel.lab.catalyst.bootstrap_cache import _BootstrapCache

class Config:

    SECTIONS = ['app', 'auth', 'cache', 'cors', 'database', 'filesystems', 'logging', 'mail', 'queue', 'session','bootstrap']

    @staticmethod
    def get(section: str, dot_values: str = None):
        if section not in Config.SECTIONS:
            raise KeyError(f"The section '{section}' is not found in the configuration.")

        config_app = _BootstrapCache().get_config()
        if not dot_values:
            return config_app.get(section)

        data = dot_values.split('.')

        # Initialize index to the specific section of the configuration
        index = config_app.get(section)
        if index is None:
            raise KeyError(f"The section '{section}' is empty or not found in the configuration.")

        # Access nested values using the dot_values data
        for key in data:
            index = index.get(key)
            if index is None:
                raise KeyError(f"The key '{key}' is not found in the configuration under section '{section}'.")

        return index

    @staticmethod
    def app(value: str = None):
        return Config.get('app', value)

    @staticmethod
    def auth(value: str = None):
        return Config.get('auth', value)

    @staticmethod
    def cache(value: str = None):
        return Config.get('cache', value)

    @staticmethod
    def cors(value: str = None):
        return Config.get('cors', value)

    @staticmethod
    def database(value: str = None):
        return Config.get('database', value)

    @staticmethod
    def filesystems(value: str = None):
        return Config.get('filesystems', value)

    @staticmethod
    def logging(value: str = None):
        return Config.get('logging', value)

    @staticmethod
    def mail(value: str = None):
        return Config.get('mail', value)

    @staticmethod
    def queue(value: str = None):
        return Config.get('queue', value)

    @staticmethod
    def session(value: str = None):
        return Config.get('session', value)

    @staticmethod
    def bootstrap(value: str = None):
        return Config.get('bootstrap', value)
