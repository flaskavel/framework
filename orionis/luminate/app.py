from orionis.luminate.container.container import Container
from orionis.luminate.bootstrap.config_bootstrapper import ConfigBootstrapper
from orionis.luminate.bootstrap.command_bootstrapper import CommandsBootstrapper
from orionis.luminate.patterns.singleton import SingletonMeta

class Application(metaclass=SingletonMeta):

    def __init__(self):

        self._config = {}
        self._commands = {}

        self.container = Container()
        self.container.instance(self.container)
        self._bootstraping()

    def _bootstraping(self):
        config_bootstrapper_key = self.container.singleton(ConfigBootstrapper)
        config_bootstrapper: ConfigBootstrapper = self.container.make(config_bootstrapper_key)
        self._config = config_bootstrapper.get()

        commands_bootstrapper_key = self.container.singleton(CommandsBootstrapper)
        commands_bootstrapper: CommandsBootstrapper = self.container.make(commands_bootstrapper_key)
        self._commands = commands_bootstrapper.get()
        print(self._commands)

    def isBooted(self):
        return True