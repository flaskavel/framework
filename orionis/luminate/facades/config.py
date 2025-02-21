from orionis.luminate.container.container import Container
from orionis.luminate.cache.app.config import CacheConfig
from orionis.luminate.orionis import Orionis, OrionisContext

class Config:

    @staticmethod
    def get():
        with OrionisContext() as orionis:
            cont = Container()
            return cont.make(CacheConfig).config
