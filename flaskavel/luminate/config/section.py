from enum import Enum

class Section(Enum):
    """
    Enum representing different configuration sections in the application.
    """
    APP = 'app'
    AUTH = 'auth'
    CACHE = 'cache'
    CORS = 'cors'
    DATABASE = 'database'
    FILESYSTEMS = 'filesystems'
    LOGGING = 'logging'
    MAIL = 'mail'
    SESSION = 'session'