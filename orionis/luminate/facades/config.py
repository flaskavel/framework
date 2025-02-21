from orionis.luminate.container.container import Container
from orionis.luminate.cache.app.config import CacheConfig
from orionis.luminate.orionis import OrionisContext

class Config:

    @staticmethod
    def get():
        with OrionisContext() as ctx:
            return ctx.make(CacheConfig).config
