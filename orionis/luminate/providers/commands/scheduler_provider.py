from orionis.luminate.providers.service_provider import ServiceProvider
from orionis.luminate.services.commands.scheduler_service import ScheduleService

class ScheduleServiceProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers services or bindings into the given container.
        """
        self._container_id = self.app.scoped(ScheduleService)

    def boot(self,) -> None:
        """
        Boot the service provider.

        This method is intended to be overridden by subclasses to perform
        any necessary bootstrapping or initialization tasks.
        """
        self.app.make(self._container_id)