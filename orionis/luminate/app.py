from orionis.luminate.container.container import Container

class App:

    def __init__(self):
        # Inicializa el contenedor de dependencias
        self.container = Container()

    def start(self):
        pass

    def finish(self):
        pass

    def in_context(self):
        """Método placeholder para gestionar el contexto de la aplicación"""
        pass

    def register_service_providers(self):
        """
        Registra los proveedores de servicios en el contenedor.
        Carga y registra los servicios de forma perezosa.
        """
        # Importación perezosa de los servicios
        from orionis.luminate.cache.app.config import CacheConfig
        from orionis.luminate.bootstrap.config.register import Register
        from orionis.luminate.bootstrap.config.bootstrapper import Bootstrapper

        # Registro de servicios esenciales en el contenedor
        self.container.singleton(CacheConfig)  # Configuración del cache
        self.container.singleton(Register)    # Registro de la configuración de la app
        self.container.singleton(Bootstrapper)  # Inicialización del sistema

    def load_config(self):
        """Método placeholder para cargar la configuración de la aplicación"""
        pass
