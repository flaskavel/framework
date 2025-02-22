from orionis.luminate.app_context import AppContext
from orionis.luminate.cache.app.config import CacheConfig

class Config:

    @staticmethod
    def get():
        with AppContext() as app:
            cache = app.container.make(CacheConfig)
            return cache.config
