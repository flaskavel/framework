from orionis.luminate.container.container import Container
from orionis.luminate.cache.app.config import CacheConfig
from orionis.luminate.app import OrionisContext

class Config:

    @staticmethod
    def get():
        with OrionisContext() as ctx:
            return ctx.container.make(CacheConfig).config
