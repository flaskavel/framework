class Config:

    def __init__(self, cache=None):
        """
        Initializes the Register instance and prepares the cache commands system.
        """
        self.cache_config = cache

    def load(self, command_class):
        pass

bootstrap = Config()