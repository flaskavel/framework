from orionis.luminate.providers.service_provider import ServiceProvider
from orionis.luminate.services.config.config_service import ConfigService

class ConfigServiceProvider(ServiceProvider):

    def register(self, config: dict = {}) -> None:
        """
        Registers services or bindings into the given container.
        """
        config = ConfigService(config)
        self._container_id = self.app.instance(config)

    def boot(self,) -> None:
        """
        Boot the service provider.

        This method is intended to be overridden by subclasses to perform
        any necessary bootstrapping or initialization tasks.
        """
        pass