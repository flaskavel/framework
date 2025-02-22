import traceback
from orionis.luminate.container.container import Container
from orionis.luminate.bootstrap.config_bootstrapper import ConfigBootstrapper
from orionis.luminate.patterns.singleton import SingletonMeta

class Application(metaclass=SingletonMeta):

    def __init__(self):
        self.container = Container()
        self.container.instance(self.container)
        self._bootstraping()

    def _bootstraping(self):
        config_bootstrapper = self.container.singleton(ConfigBootstrapper)
        config = self.container.make(config_bootstrapper)
        print(config)

    def isBooted(self):
        return True