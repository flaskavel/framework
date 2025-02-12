from typing import Protocol

class IApp(Protocol):
    """
    Interface that enforces the required properties for an application configuration.

    Attributes
    ----------
    name : str
        The name of the application, useful for notifications and UI elements.
    debug : bool
        Determines if debug mode is enabled, providing detailed error information.
    bytecode : bool
        Specifies whether the application should generate bytecode files.
    timezone : str
        Defines the application's timezone.
    url : str
        The application's base URL.
    port : int
        The port on which the application runs.
    cipher : str
        Defines the encryption algorithm used by the application.
    key : str
        The encryption key used for securing data.
    """

    name: str
    debug: bool
    bytecode: bool
    timezone: str
    url: str
    port: int
    cipher: str
    key: str