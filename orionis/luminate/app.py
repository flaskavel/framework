from orionis.luminate.container.container import Container
from orionis.luminate.bootstrap.config_bootstrapper import ConfigBootstrapper
from orionis.luminate.bootstrap.command_bootstrapper import CommandsBootstrapper
from orionis.luminate.bootstrap.environment_bootstrapper import EnvironmentBootstrapper
from orionis.luminate.patterns.singleton import SingletonMeta
from orionis.luminate.providers.environment.environment__service_provider import EnvironmentServiceProvider
from orionis.luminate.providers.config.config_service_provider import ConfigServiceProvider
from orionis.luminate.services.config.config_service import ConfigService

class Application(metaclass=SingletonMeta):

    def __init__(self, container: Container):

        # Atributos de la clase
        self._config = {}
        self._commands = {}
        self._environment_vars = {}

        # Inicializar el contenedor de la aplicacion
        self.container = container
        self.container.instance(container)

        # Cargar el servidor de entorno
        self._loadServiceProviderEnvironment()

        # Cargar dinamicamente la configurcion de la aplicacion.
        self._bootstraping()

        # Registrrar los comandos en el contenedor
        self._registerCommands()

        # Cargar de provedores core
        self._loadServiceProviderCore()

    def _loadServiceProviderEnvironment(self):

        # Cargar el proveedor de entorno
        _environment_provider = EnvironmentServiceProvider(app=self.container)
        _environment_provider.register()
        _environment_provider.boot()

    def _bootstraping(self):

        # Cargar la configuracion de la aplicacion
        config_bootstrapper_key = self.container.singleton(ConfigBootstrapper)
        config_bootstrapper: ConfigBootstrapper = self.container.make(config_bootstrapper_key)
        self._config = config_bootstrapper.get()

        # Cargar los comandos propios y definidos por el desarrollador
        commands_bootstrapper_key = self.container.singleton(CommandsBootstrapper)
        commands_bootstrapper: CommandsBootstrapper = self.container.make(commands_bootstrapper_key)
        self._commands = commands_bootstrapper.get()

        # Cargar las variables de entorno solo desde el archivo .env (No se carga desde el sistema operativo, por seguridad)
        environment_bootstrapper_key = self.container.singleton(EnvironmentBootstrapper)
        environment_bootstrapper: EnvironmentBootstrapper = self.container.make(environment_bootstrapper_key)
        self._environment_vars = environment_bootstrapper.get()

    def _registerCommands(self):

        # Registrar los comandos en el contenedor
        for command in self._commands:
            _key_instance_container = self.container.bind(self._commands[command].get('concrete'))
            self.container.alias(alias=command, concrete=_key_instance_container)

    def _loadServiceProviderCore(self):

        # Cargar el proveedor de configuracion
        _environment_provider = ConfigServiceProvider(app=self.container)
        _environment_provider.register(config=self._config)
        _environment_provider.boot()