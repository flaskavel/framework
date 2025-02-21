from orionis.luminate.container.container import Container
from orionis.luminate.cache.app.config import CacheConfig
from orionis.luminate.bootstrap.config.register import Register
from orionis.luminate.bootstrap.config.bootstrapper import Bootstrapper

class App:

    def __init__(self):
        self.container = Container()

    def start(self):
        self._register_config_providers()
        self._resolve_config_providers()

    def finish(self):
        self.container = None

    def _register_config_providers(self):
        self.container.singleton(CacheConfig)
        self.container.singleton(Register)
        self.container.singleton(Bootstrapper)

    def _resolve_config_providers(self):
        self.container.make(Register)
        self.container.make(Bootstrapper)
