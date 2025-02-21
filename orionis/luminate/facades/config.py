from orionis.luminate.container.container import Container
from orionis.luminate.cache.app.config import CacheConfig
from orionis.luminate.orionis import Orionis

class Config:

    @staticmethod
    def get():

        if Orionis().isStarted():
            cont = Container()
            return cont.make(CacheConfig).config

        raise Exception("The application cannot be executed correctly within the Orionis Framework context.")