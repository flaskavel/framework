from orionis.luminate.container.container import Container

class ServiceProvidersBootstrapper:

    def __init__(self, container : Container) -> None:
        self._container = container
        self._autoload()

    def _autoload(self) -> None:
        pass